# evaluation/test_cases.py

# ============================================================
# TEST CASES
#
# Each test can evaluate:
# - Tool routing
# - Tool arguments
# - Metric selection
# - Answer correctness
# - Document grounding
# - Error handling
# - Hallucination avoidance
# - Conversation memory
# ============================================================


TEST_CASES = [

    # ========================================================
    # 1. GET_DATE
    # ========================================================

    {
        "id": 1,
        "scenario": "current_date",
        "question": "What is today's date?",
        "expected_tools": ["get_date"],
        "answer_type": "date",
    },

    {
        "id": 2,
        "scenario": "relative_date",
        "question": "What date was two weeks ago?",
        "expected_tools": ["get_date"],
        "answer_type": "date",
    },

    {
        "id": 3,
        "scenario": "relative_date_month",
        "question": "What date was one month ago?",
        "expected_tools": ["get_date"],
        "answer_type": "date",
    },


    # ========================================================
    # 2. RETRIEVE_DOCUMENTS / RAG
    # ========================================================

    {
        "id": 4,
        "scenario": "rag_business_segments",
        "question": "What are Amazon's main business segments?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "North America",
            "International",
            "AWS",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 5,
        "scenario": "rag_revenue_2025",
        "question": "What was Amazon's revenue in 2025?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "revenue",
            "716",
            "924",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 6,
        "scenario": "rag_net_income",
        "question": "What was Amazon's net income in 2025?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "net income",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 7,
        "scenario": "rag_total_assets",
        "question": "What were Amazon's total assets in 2025?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "total assets",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 8,
        "scenario": "rag_operating_cash_flow",
        "question": "What does Amazon's 2025 10-K say about operating cash flow?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "operating",
            "cash",
            "flow",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 9,
        "scenario": "rag_aws",
        "question": "What does Amazon's 2025 10-K say about AWS?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "AWS",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 10,
        "scenario": "rag_risks",
        "question": "What risks does Amazon identify in its 2025 10-K?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "risk",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 11,
        "scenario": "rag_specific_filing",
        "question": "According to Amazon's 2024 10-K, what was its revenue?",
        "expected_tools": ["retrieve_documents"],
        "expected_keywords": [
            "2024",
            "revenue",
        ],
        "requires_document_grounding": True,
    },


    # ========================================================
    # 3. GET_COMPANY_STOCK_INFO
    # ========================================================

    {
        "id": 12,
        "scenario": "stock_single_day",
        "question": "Give me Amazon's stock data for September 15, 2026.",
        "expected_tools": ["get_company_stock_info"],
        "expected_tickers": ["AMZN"],
        "answer_type": "stock_data",
    },

    {
        "id": 13,
        "scenario": "stock_date_range",
        "question": (
            "Give me Amazon's stock data "
            "from September 1 to September 10, 2026."
        ),
        "expected_tools": ["get_company_stock_info"],
        "expected_tickers": ["AMZN"],
        "answer_type": "stock_data",
    },

    {
        "id": 14,
        "scenario": "stock_ohlcv",
        "question": (
            "Give me Amazon's OHLCV data "
            "from September 1 to September 10, 2026."
        ),
        "expected_tools": ["get_company_stock_info"],
        "expected_tickers": ["AMZN"],
        "expected_keywords": [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
        "answer_type": "stock_data",
    },

    {
        "id": 15,
        "scenario": "multiple_companies",
        "question": (
            "Give me the closing prices for "
            "Amazon, Nvidia, and Apple from "
            "September 1 to September 5, 2026."
        ),
        "expected_tools": ["get_company_stock_info"],
        "expected_tickers": [
            "AMZN",
            "NVDA",
            "AAPL",
        ],
        "answer_type": "stock_data",
    },

    {
        "id": 16,
        "scenario": "weekend_boundary",
        "question": (
            "Give me Amazon's stock data "
            "from September 1 to October 4, 2026."
        ),
        "expected_tools": ["get_company_stock_info"],
        "expected_tickers": ["AMZN"],
        "answer_type": "stock_data",
        # October 4, 2026 is a Sunday.
        # The response should use available trading days.
    },

    {
        "id": 17,
        "scenario": "stock_specific_close",
        "question": (
            "What was Amazon's closing price "
            "on September 15, 2026?"
        ),
        "expected_tools": ["get_company_stock_info"],
        "expected_tickers": ["AMZN"],
        "calculate_ground_truth": True,
        "metric": "single_day_close",
        "tolerance": 0.01,
    },


    # ========================================================
    # 4. COMPANY_METRICS
    # ========================================================

    {
        "id": 18,
        "scenario": "highest_close",
        "question": (
            "What was Amazon's highest closing price "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "highest_close",
        "calculate_ground_truth": True,
        "metric": "highest_close",
        "tolerance": 0.01,
    },

    {
        "id": 19,
        "scenario": "lowest_close",
        "question": (
            "What was Amazon's lowest closing price "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "lowest_close",
        "calculate_ground_truth": True,
        "metric": "lowest_close",
        "tolerance": 0.01,
    },

    {
        "id": 20,
        "scenario": "average_close",
        "question": (
            "What was Amazon's average closing price "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "average_close",
        "calculate_ground_truth": True,
        "metric": "average_close",
        "tolerance": 0.01,
    },

    {
        "id": 21,
        "scenario": "highest_high",
        "question": (
            "What was Amazon's highest intraday price "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "highest_high",
        "calculate_ground_truth": True,
        "metric": "highest_high",
        "tolerance": 0.01,
    },

    {
        "id": 22,
        "scenario": "lowest_low",
        "question": (
            "What was Amazon's lowest intraday price "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "lowest_low",
        "calculate_ground_truth": True,
        "metric": "lowest_low",
        "tolerance": 0.01,
    },

    {
        "id": 23,
        "scenario": "average_high",
        "question": (
            "What was Amazon's average daily high "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "average_high",
        "calculate_ground_truth": True,
        "metric": "average_high",
        "tolerance": 0.01,
    },

    {
        "id": 24,
        "scenario": "average_low",
        "question": (
            "What was Amazon's average daily low "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "average_low",
        "calculate_ground_truth": True,
        "metric": "average_low",
        "tolerance": 0.01,
    },

    {
        "id": 25,
        "scenario": "average_volume",
        "question": (
            "What was Amazon's average trading volume "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "average_volume",
        "calculate_ground_truth": True,
        "metric": "average_volume",
        "tolerance": 1,
    },

    {
        "id": 26,
        "scenario": "price_change",
        "question": (
            "How much did Amazon's stock price change "
            "during September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "price_change",
        "calculate_ground_truth": True,
        "metric": "price_change",
        "tolerance": 0.01,
    },

    {
        "id": 27,
        "scenario": "percentage_change",
        "question": (
            "What percentage did Amazon's stock change "
            "during September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "percentage_change",
        "calculate_ground_truth": True,
        "metric": "percentage_change",
        "tolerance": 0.01,
    },


    # ========================================================
    # 5. RELATIVE DATE + STOCK
    # ========================================================

    {
        "id": 28,
        "scenario": "relative_stock_date",
        "question": "What was Amazon's closing price yesterday?",
        "expected_tools": [
            "get_date",
            "get_company_stock_info",
        ],
        "expected_tickers": ["AMZN"],
        "calculate_ground_truth": True,
        "metric": "single_day_close",
        "relative_period": "yesterday",
        "tolerance": 0.01,
    },

    {
        "id": 29,
        "scenario": "relative_highest",
        "question": (
            "What was Amazon's highest closing price "
            "last month?"
        ),
        "expected_tools": [
            "get_date",
            "company_metrics",
        ],
        "expected_metric": "highest_close",
        "calculate_ground_truth": True,
        "metric": "highest_close",
        "relative_period": "last_month",
        "tolerance": 0.01,
    },

    {
        "id": 30,
        "scenario": "relative_lowest",
        "question": (
            "What was Amazon's lowest closing price "
            "last month?"
        ),
        "expected_tools": [
            "get_date",
            "company_metrics",
        ],
        "expected_metric": "lowest_close",
        "calculate_ground_truth": True,
        "metric": "lowest_close",
        "relative_period": "last_month",
        "tolerance": 0.01,
    },

    {
        "id": 31,
        "scenario": "relative_stock_range",
        "question": (
            "Give me Amazon's closing prices "
            "for the last two months."
        ),
        "expected_tools": [
            "get_date",
            "get_company_stock_info",
        ],
        "expected_tickers": ["AMZN"],
        "answer_type": "stock_data",
    },


    # ========================================================
    # 6. TOOL ROUTING
    # ========================================================

    {
        "id": 32,
        "scenario": "routing_stock_metric",
        "question": (
            "What was Amazon's highest closing price "
            "in September 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "must_not_use": [
            "retrieve_documents",
            "get_company_stock_info",
        ],
        "expected_metric": "highest_close",
        "calculate_ground_truth": True,
        "metric": "highest_close",
        "tolerance": 0.01,
    },

    {
        "id": 33,
        "scenario": "routing_rag",
        "question": (
            "What risks does Amazon identify "
            "in its 2025 10-K?"
        ),
        "expected_tools": ["retrieve_documents"],
        "must_not_use": [
            "company_metrics",
            "get_company_stock_info",
        ],
        "requires_document_grounding": True,
    },

    {
        "id": 34,
        "scenario": "routing_raw_stock",
        "question": (
            "Give me Amazon's daily closing prices "
            "from September 1 to September 10, 2026."
        ),
        "expected_tools": [
            "get_company_stock_info",
        ],
        "must_not_use": [
            "retrieve_documents",
            "company_metrics",
        ],
        "expected_tickers": ["AMZN"],
        "answer_type": "stock_data",
    },


    # ========================================================
    # 7. MULTI-TOOL QUESTIONS
    # ========================================================

    {
        "id": 35,
        "scenario": "rag_plus_metrics",
        "question": (
            "What was Amazon's revenue in 2025 "
            "and what was its percentage stock change "
            "in September 2026?"
        ),
        "expected_tools": [
            "retrieve_documents",
            "company_metrics",
        ],
        "expected_metric": "percentage_change",
        "calculate_ground_truth": True,
        "metric": "percentage_change",
        "tolerance": 0.01,
        "requires_document_grounding": True,
    },

    {
        "id": 36,
        "scenario": "date_plus_metric",
        "question": (
            "What was Amazon's highest closing price "
            "last month?"
        ),
        "expected_tools": [
            "get_date",
            "company_metrics",
        ],
        "expected_metric": "highest_close",
        "calculate_ground_truth": True,
        "metric": "highest_close",
        "relative_period": "last_month",
        "tolerance": 0.01,
    },

    {
        "id": 37,
        "scenario": "date_plus_stock",
        "question": (
            "Give me Amazon's closing prices "
            "for the last two months."
        ),
        "expected_tools": [
            "get_date",
            "get_company_stock_info",
        ],
        "expected_tickers": ["AMZN"],
        "answer_type": "stock_data",
    },


    # ========================================================
    # 8. NO TOOL REQUIRED
    # ========================================================

    {
        "id": 38,
        "scenario": "general_finance",
        "question": (
            "What is the difference between "
            "revenue and profit?"
        ),
        "expected_tools": [],
        "must_not_use": [
            "get_date",
            "retrieve_documents",
            "get_company_stock_info",
            "company_metrics",
        ],
        "expected_keywords": [
            "revenue",
            "profit",
        ],
    },

    {
        "id": 39,
        "scenario": "market_cap",
        "question": "What does market capitalization mean?",
        "expected_tools": [],
        "must_not_use": [
            "get_date",
            "retrieve_documents",
            "get_company_stock_info",
            "company_metrics",
        ],
        "expected_keywords": [
            "market",
            "capitalization",
        ],
    },

    {
        "id": 40,
        "scenario": "ten_k_definition",
        "question": "What is a 10-K filing?",
        "expected_tools": [],
        "must_not_use": [
            "get_date",
            "retrieve_documents",
            "get_company_stock_info",
            "company_metrics",
        ],
        "expected_keywords": [
            "10-K",
            "SEC",
        ],
    },


    # ========================================================
    # 9. ERROR HANDLING
    # ========================================================

    {
        "id": 41,
        "scenario": "invalid_date_range",
        "question": (
            "What was Amazon's lowest closing price "
            "from September 10, 2026 to September 1, 2026?"
        ),
        "expected_tools": ["company_metrics"],
        "expected_metric": "lowest_close",
        "expected_result": "error",
    },

    {
        "id": 42,
        "scenario": "invalid_ticker",
        "question": (
            "Give me the stock data for XYZ123 "
            "from September 1 to September 5, 2026."
        ),
        "expected_tools": [
            "get_company_stock_info",
        ],
        "expected_result": "error",
    },

    {
        "id": 43,
        "scenario": "non_trading_day",
        "question": (
            "What was Amazon's stock price "
            "on Sunday, October 4, 2026?"
        ),
        "expected_tools": [
            "get_company_stock_info",
        ],
        "expected_tickers": ["AMZN"],
        "expected_result": "no_trading_data",
    },


    # ========================================================
    # 10. RAG OUT-OF-SCOPE / HALLUCINATION
    # ========================================================

    {
        "id": 44,
        "scenario": "unknown_company_rag",
        "question": (
            "What does Apple's 2025 10-K say "
            "about its revenue?"
        ),
        "expected_tools": ["retrieve_documents"],
        "expected_result": "not_found",
        "must_not_contain": [
            "Apple's 2025 revenue was",
            "Apple's revenue was",
        ],
    },

    {
        "id": 45,
        "scenario": "unsupported_information",
        "question": (
            "What does Amazon's 10-K say about "
            "its operations on Mars?"
        ),
        "expected_tools": ["retrieve_documents"],
        "expected_result": "not_found",
        "must_not_contain": [
            "Amazon operates on Mars",
            "Amazon has operations on Mars",
            "Amazon's Mars division",
        ],
    },


    # ========================================================
    # 11. AMBIGUOUS QUESTIONS
    # ========================================================

    {
        "id": 46,
        "scenario": "ambiguous_price",
        "question": "What was Amazon's price last month?",
        "expected_tools": [
            "get_date",
            "get_company_stock_info",
        ],
        "expected_tickers": ["AMZN"],
        "answer_type": "stock_data",
    },

    {
        "id": 47,
        "scenario": "ambiguous_performance",
        "question": "How did Amazon perform last month?",
        "expected_tools": [
            "get_date",
            "company_metrics",
        ],
        "expected_metric": "percentage_change",
        "calculate_ground_truth": True,
        "metric": "percentage_change",
        "relative_period": "last_month",
        "tolerance": 0.01,
    },


    # ========================================================
    # 12. CONVERSATION / MEMORY
    # ========================================================

    {
        "id": 48,
        "scenario": "conversation_followup",
        "conversation": [
            "What was Amazon's highest closing price in September 2026?",
            "What about August?",
        ],
        "expected_tools": [
            "company_metrics",
        ],
        "expected_metric": "highest_close",
        "calculate_ground_truth": True,
        "metric": "highest_close",
        "tolerance": 0.01,
    },

    {
        "id": 49,
        "scenario": "conversation_context",
        "conversation": [
            "What was Amazon's lowest closing price in September 2026?",
            "And what was the highest?",
        ],
        "expected_tools": [
            "company_metrics",
        ],
        "expected_metric": "highest_close",
        "calculate_ground_truth": True,
        "metric": "highest_close",
        "tolerance": 0.01,
    },


    # ========================================================
    # 13. COMBINED FACT-CHECK
    # ========================================================

    {
        "id": 50,
        "scenario": "combined_financial_answer",
        "question": (
            "According to Amazon's 2025 10-K, "
            "what was its revenue, and what was "
            "its highest closing price in September 2026?"
        ),

        "expected_tools": [
            "retrieve_documents",
            "company_metrics",
        ],

        "expected_metric": "highest_close",

        # Stock portion
        "calculate_ground_truth": True,
        "metric": "highest_close",
        "tolerance": 0.01,

        # Filing portion
        "expected_keywords": [
            "revenue",
            "716",
            "924",
        ],

        "requires_document_grounding": True,
    },
]