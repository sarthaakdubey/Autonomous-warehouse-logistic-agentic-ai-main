import re
from backend.rag.db import get_collection
from backend.crew.crew_runner import run_crew
from backend.memory.memory_store import get_memory


def is_dataset_query(question: str) -> bool:
    question = question.lower()

    research_words = [
        "improve", "optimize", "why",
        "strategy", "recommend",
        "how to", "best practice",
        "automation"
    ]

    for word in research_words:
        if word in question:
            return False

    return True


def extract_order_id(question: str):
    match = re.search(r"\b\d{4}\b", question)
    return match.group() if match else None


def parse_document(doc: str):
    """
    Safely parse a document string into dictionary.
    """
    values = {}
    try:
        pairs = [item.split(":", 1) for item in doc.split(", ")]
        for pair in pairs:
            if len(pair) == 2:
                values[pair[0].strip()] = pair[1].strip()
    except:
        pass
    return values


def analyze_warehouse(question: str):

    # ====================================
    # DATASET MODE
    # ====================================
    if is_dataset_query(question):

        collection = get_collection()
        q_lower = question.lower()
        order_id = extract_order_id(question)

        # --------------------------------
        # 1️⃣ Specific Order Lookup
        # --------------------------------
        if order_id:
            results = collection.get()
            documents = results.get("documents", [])

            documents = [
                doc for doc in documents
                if f"order_id:{order_id}" in doc
            ]

            if not documents:
                return {
                    "success": True,
                    "status": ["Dataset lookup mode"],
                    "result": f"No order found with ID {order_id}"
                }

        # --------------------------------
        # 2️⃣ Aggregation Queries (FULL DATASET)
        # --------------------------------
        elif any(word in q_lower for word in [
            "highest delay", "most delay", "maximum delay",
            "lowest delay", "least delay", "minimum delay",
            "average delay", "total delay",
            "rank", "ranking"
        ]):
            results = collection.get()
            documents = results.get("documents", [])

        # --------------------------------
        # 3️⃣ All Orders
        # --------------------------------
        elif "all orders" in q_lower or "list orders" in q_lower:
            results = collection.get()
            documents = results.get("documents", [])

        # --------------------------------
        # 4️⃣ Semantic Fallback
        # --------------------------------
        else:
            results = collection.query(
                query_texts=[question],
                n_results=20
            )
            documents = results.get("documents", [[]])[0]

        if not documents:
            return {
                "success": True,
                "status": ["Dataset lookup mode"],
                "result": "No matching records found."
            }

        # ====================================
        # PARSE DATASET
        # ====================================
        warehouse_delay_map = {}
        parsed_rows = []

        for doc in documents:
            values = parse_document(doc)

            if not values:
                continue

            warehouse = values.get("warehouse", "").strip().title()

            delay_raw = (
                values.get("delay")
                or values.get("delay_minutes")
                or values.get("delay_min")
                or "0"
            )

            number_match = re.search(r"\d+", str(delay_raw))
            delay_value = int(number_match.group()) if number_match else 0

            if warehouse:
                warehouse_delay_map.setdefault(warehouse, []).append(delay_value)

            parsed_rows.append((warehouse, delay_value, values))

        # ====================================
        # ANALYTICAL OPERATIONS
        # ====================================

        # 🔥 Highest Delay
        if "highest delay" in q_lower or "most delay" in q_lower:
            if not warehouse_delay_map:
                return {
                    "success": True,
                    "status": ["Dataset lookup mode"],
                    "result": "No delay data available."
                }

            highest = max(
                warehouse_delay_map.items(),
                key=lambda x: max(x[1])
            )

            return {
                "success": True,
                "status": ["Dataset lookup mode"],
                "result": f"{highest[0]} has the highest delay."
            }

        # 🔥 Lowest Delay
        if "lowest delay" in q_lower or "least delay" in q_lower:
            if not warehouse_delay_map:
                return {
                    "success": True,
                    "status": ["Dataset lookup mode"],
                    "result": "No delay data available."
                }

            lowest = min(
                warehouse_delay_map.items(),
                key=lambda x: min(x[1])
            )

            return {
                "success": True,
                "status": ["Dataset lookup mode"],
                "result": f"{lowest[0]} has the lowest delay."
            }

        # 🔥 Average Delay
        if "average delay" in q_lower:
            all_delays = [d for delays in warehouse_delay_map.values() for d in delays]

            if not all_delays:
                return {
                    "success": True,
                    "status": ["Dataset lookup mode"],
                    "result": "No delay data available."
                }

            avg = sum(all_delays) / len(all_delays)

            return {
                "success": True,
                "status": ["Dataset lookup mode"],
                "result": f"Average delay across all warehouses is {round(avg, 2)}."
            }

        # 🔥 Total Delay Per Warehouse
        if "total delay" in q_lower:
            result_text = "Total delay per warehouse:\n"
            for wh, delays in warehouse_delay_map.items():
                result_text += f"{wh} → {sum(delays)}\n"

            return {
                "success": True,
                "status": ["Dataset lookup mode"],
                "result": result_text
            }

        # 🔥 Ranking
        if "rank" in q_lower or "ranking" in q_lower:
            ranking = sorted(
                warehouse_delay_map.items(),
                key=lambda x: sum(x[1]),
                reverse=True
            )

            result_text = "Warehouse Ranking (Highest to Lowest Total Delay):\n"
            for i, (wh, delays) in enumerate(ranking, start=1):
                result_text += f"{i}. {wh} → {sum(delays)}\n"

            return {
                "success": True,
                "status": ["Dataset lookup mode"],
                "result": result_text
            }

        # ====================================
        # DEFAULT TABLE OUTPUT
        # ====================================
        table = "| Order ID | Warehouse | Product | Quantity | Distance (km) | Transport Mode | Delay | Picking Time (min) |\n"
        table += "|----------|-----------|---------|----------|---------------|----------------|-------|-------------------|\n"

        for _, _, values in parsed_rows:
            table += (
                f"| {values.get('order_id','')} "
                f"| {values.get('warehouse','')} "
                f"| {values.get('product','')} "
                f"| {values.get('quantity','')} "
                f"| {values.get('distance_km','')} "
                f"| {values.get('transport_mode','')} "
                f"| {values.get('delay','')} "
                f"| {values.get('picking_time_min','')} |\n"
            )

        return {
            "success": True,
            "status": ["Dataset lookup mode"],
            "result": table
        }

    # ====================================
    # ANALYTICAL MODE (Crew AI)
    # ====================================
    from backend.rag.retriever import retrieve_context

    context = retrieve_context(question)
    memory = get_memory(question)

    enhanced_prompt = f"""
Warehouse Dataset Context:
{context}

Past Conversation Memory:
{memory}

User Question:
{question}
"""

    return run_crew(enhanced_prompt, question)