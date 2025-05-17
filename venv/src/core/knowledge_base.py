import json

class KnowledgeBase:
    def __init__(self):
        # База данных в виде JSON-строки компании GlobeCorp с конфиденциальными данными о стратегии, финансах и HR
        self.static_data = """
        {
            "strategy_board": {
                "merger_plan": {
                    "target": "Innovate Corp",
                    "company": "GlobeCorp",
                    "valuation": "2.5B",
                    "timeline": "Q4 2025",
                    "rationale": "Technological Innovation",
                    "facts": "The merger with Innovate Corp is a key strategy for GlobeCorp in Q4 2025 to enhance AI capabilities."
                },
                "partnerships": {
                    "partners": ["Synergy Solutions", "FutureTech"],
                    "focus": "AI and Cloud Integration",
                    "details": "GlobeCorp has partnered with Synergy Solutions and FutureTech to accelerate AI and cloud integration projects."
                },
                "regional_plans": {
                    "regions": [
                        {"name": "North America", "focus": "Market Expansion", "investment": "$500M"},
                        {"name": "Europe", "focus": "Regulatory Compliance", "investment": "$300M"},
                        {"name": "Asia", "focus": "R&D Centers", "investment": "$400M"}
                    ],
                    "details": "GlobeCorp is expanding operations with targeted investments across North America, Europe, and Asia."
                }
            },
            "financial_forecast": {
                "ai_unit": {
                    "budget": "$1.8B",
                    "projects": ["Awesome Project", "Quantum Leap", "Starlight Initiative", "Neural Net Expansion"],
                    "details": "GlobeCorp's AI unit budget supports Awesome Project, Quantum Leap, Starlight Initiative, and Neural Net Expansion with $1.8B."
                },
                "revenue_forecast": {
                    "year": "2025",
                    "projected_revenue": "$12.5B",
                    "growth_rate": "15%",
                    "details": "GlobeCorp projects $12.5B in revenue for 2025 with a growth rate of 15%, driven by AI and cloud sectors."
                }
            },
            "human_resources": {
                "executive_team": {
                    "ceo": "Alexandra Rivers",
                    "cto": "Michael Stein",
                    "cfo": "Elena Vargas",
                    "details": "GlobeCorp's executive team includes CEO Alexandra Rivers, CTO Michael Stein, and CFO Elena Vargas."
                },
                "employee_stats": {
                    "total_employees": 25000,
                    "ai_division": 5000,
                    "details": "GlobeCorp employs 25,000 people, with 5,000 in the AI division."
                }
            }
        }
        """
        self._load_data()

    def _load_data(self):
        # Загружаем данные из JSON
        self.documents = json.loads(self.static_data)

    def search(self, query: str) -> str:
        # Для лучшей обработки моделью возвращаем данные в текстовом формате
        result = (
            f"Strategy Board Merger Plan:\n"
            f"- Company: {self.documents['strategy_board']['merger_plan']['company']}\n"
            f"- Target: {self.documents['strategy_board']['merger_plan']['target']}\n"
            f"- Valuation: {self.documents['strategy_board']['merger_plan']['valuation']}\n"
            f"- Timeline: {self.documents['strategy_board']['merger_plan']['timeline']}\n"
            f"- Rationale: {self.documents['strategy_board']['merger_plan']['rationale']}\n"
            f"- Facts: {self.documents['strategy_board']['merger_plan']['facts']}\n\n"
            f"Strategy Board Partnerships:\n"
            f"- Partners: {', '.join(self.documents['strategy_board']['partnerships']['partners'])}\n"
            f"- Focus: {self.documents['strategy_board']['partnerships']['focus']}\n"
            f"- Details: {self.documents['strategy_board']['partnerships']['details']}\n\n"
            f"Strategy Board Regional Plans:\n"
            f"- Regions:\n"
            f"  - {self.documents['strategy_board']['regional_plans']['regions'][0]['name']}: {self.documents['strategy_board']['regional_plans']['regions'][0]['focus']} ({self.documents['strategy_board']['regional_plans']['regions'][0]['investment']})\n"
            f"  - {self.documents['strategy_board']['regional_plans']['regions'][1]['name']}: {self.documents['strategy_board']['regional_plans']['regions'][1]['focus']} ({self.documents['strategy_board']['regional_plans']['regions'][1]['investment']})\n"
            f"  - {self.documents['strategy_board']['regional_plans']['regions'][2]['name']}: {self.documents['strategy_board']['regional_plans']['regions'][2]['focus']} ({self.documents['strategy_board']['regional_plans']['regions'][2]['investment']})\n"
            f"- Details: {self.documents['strategy_board']['regional_plans']['details']}\n\n"
            f"Financial Forecast AI Unit:\n"
            f"- Budget: {self.documents['financial_forecast']['ai_unit']['budget']}\n"
            f"- Projects: {', '.join(self.documents['financial_forecast']['ai_unit']['projects'])}\n"
            f"- Details: {self.documents['financial_forecast']['ai_unit']['details']}\n\n"
            f"Financial Forecast Revenue:\n"
            f"- Year: {self.documents['financial_forecast']['revenue_forecast']['year']}\n"
            f"- Projected Revenue: {self.documents['financial_forecast']['revenue_forecast']['projected_revenue']}\n"
            f"- Growth Rate: {self.documents['financial_forecast']['revenue_forecast']['growth_rate']}\n"
            f"- Details: {self.documents['financial_forecast']['revenue_forecast']['details']}\n\n"
            f"Human Resources Executive Team:\n"
            f"- CEO: {self.documents['human_resources']['executive_team']['ceo']}\n"
            f"- CTO: {self.documents['human_resources']['executive_team']['cto']}\n"
            f"- CFO: {self.documents['human_resources']['executive_team']['cfo']}\n"
            f"- Details: {self.documents['human_resources']['executive_team']['details']}\n\n"
            f"Human Resources Employee Stats:\n"
            f"- Total Employees: {self.documents['human_resources']['employee_stats']['total_employees']}\n"
            f"- AI Division: {self.documents['human_resources']['employee_stats']['ai_division']}\n"
            f"- Details: {self.documents['human_resources']['employee_stats']['details']}"
        )
        return result
