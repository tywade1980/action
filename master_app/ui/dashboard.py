"""
Master Dashboard - Unified Gradio UI for all systems
Provides single interface to access Deep Research, Engineering Team, and Trading Floor
"""

import gradio as gr
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime
import json


class MasterDashboard:
    """
    Unified dashboard that integrates all subsystems
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.event_log = []
        
        # Register event handler
        self.orchestrator.register_event_handler(self.handle_event)
    
    def handle_event(self, event: Dict[str, Any]):
        """Handle events from the orchestrator"""
        self.event_log.append(event)
        # Keep only last 100 events
        if len(self.event_log) > 100:
            self.event_log = self.event_log[-100:]
    
    def get_event_log_html(self) -> str:
        """Format event log as HTML"""
        if not self.event_log:
            return "<p>No events yet</p>"
        
        html = "<div style='font-family: monospace; font-size: 12px;'>"
        for event in reversed(self.event_log[-20:]):  # Show last 20
            timestamp = event.get("timestamp", "")
            event_type = event.get("type", "")
            data = event.get("data", {})
            
            color = self._get_event_color(event_type)
            html += f"<div style='color: {color}; margin: 2px 0;'>"
            html += f"[{timestamp}] {event_type}: {json.dumps(data)}"
            html += "</div>"
        html += "</div>"
        return html
    
    def _get_event_color(self, event_type: str) -> str:
        """Get color for event type"""
        colors = {
            "system_registered": "#00ff00",
            "task_started": "#00bfff",
            "task_completed": "#00ff00",
            "task_failed": "#ff0000",
            "workflow_started": "#ffff00",
            "workflow_completed": "#00ff00",
            "workflow_failed": "#ff0000",
            "knowledge_stored": "#ff00ff",
            "knowledge_retrieved": "#00ffff"
        }
        return colors.get(event_type, "#ffffff")
    
    async def execute_research(self, query: str, progress=gr.Progress()) -> str:
        """Execute a research task"""
        if not query:
            return "Please enter a research query"
        
        progress(0, desc="Creating research task...")
        
        from master_app.core.orchestrator import Task, SystemType
        task = Task(
            id=f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            system=SystemType.DEEP_RESEARCH,
            action="research",
            params={"query": query}
        )
        
        progress(0.3, desc="Executing research...")
        result = await self.orchestrator.execute_task(task)
        
        progress(1.0, desc="Complete!")
        
        if result.status == "completed":
            report = result.result.get("report", "No report generated")
            return f"## Research Results\n\n{report}"
        else:
            return f"Research failed: {result.error}"
    
    async def execute_engineering(self, requirements: str, module_name: str, progress=gr.Progress()) -> str:
        """Execute an engineering task"""
        if not requirements:
            return "Please enter requirements"
        
        if not module_name:
            module_name = "module.py"
        
        progress(0, desc="Creating engineering task...")
        
        from master_app.core.orchestrator import Task, SystemType
        task = Task(
            id=f"engineering_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            system=SystemType.ENGINEERING_TEAM,
            action="build",
            params={
                "requirements": requirements,
                "module_name": module_name,
                "class_name": "Module"
            }
        )
        
        progress(0.3, desc="Building module...")
        result = await self.orchestrator.execute_task(task)
        
        progress(1.0, desc="Complete!")
        
        if result.status == "completed":
            return f"## Engineering Results\n\nModule built successfully!\n\nCheck output directory for: {module_name}"
        else:
            return f"Engineering failed: {result.error}"
    
    async def execute_workflow(self, workflow_type: str, params_json: str, progress=gr.Progress()) -> str:
        """Execute a predefined workflow"""
        try:
            params = json.loads(params_json) if params_json else {}
        except json.JSONDecodeError:
            return "Invalid JSON parameters"
        
        progress(0, desc="Creating workflow...")
        
        from master_app.core.orchestrator import WorkflowType
        workflow_type_enum = WorkflowType[workflow_type.upper().replace(" ", "_")]
        
        workflow = self.orchestrator.create_workflow(workflow_type_enum, params)
        self.orchestrator.workflows[workflow.id] = workflow
        
        progress(0.2, desc="Executing workflow...")
        result = await self.orchestrator.execute_workflow(workflow)
        
        progress(1.0, desc="Complete!")
        
        if result.status == "completed":
            return f"## Workflow Results\n\nWorkflow completed successfully!\n\n```json\n{json.dumps(result.results, indent=2, default=str)}\n```"
        else:
            return f"Workflow failed: Check event log for details"
    
    def get_system_status(self) -> str:
        """Get system status"""
        status = self.orchestrator.get_system_status()
        
        html = "<div style='font-family: sans-serif;'>"
        html += "<h3>System Status</h3>"
        
        html += "<h4>Subsystems</h4><ul>"
        for system, state in status["systems"].items():
            color = "#00ff00" if state == "active" else "#ff0000"
            html += f"<li><span style='color: {color};'>●</span> {system}: {state}</li>"
        html += "</ul>"
        
        html += "<h4>Workflows</h4><ul>"
        html += f"<li>Total: {status['workflows']['total']}</li>"
        html += f"<li>Active: {status['workflows']['active']}</li>"
        html += f"<li>Completed: {status['workflows']['completed']}</li>"
        html += f"<li>Failed: {status['workflows']['failed']}</li>"
        html += "</ul>"
        
        html += f"<h4>Knowledge Base</h4>"
        html += f"<p>Entries: {status['knowledge_base_size']}</p>"
        
        html += "</div>"
        return html
    
    def search_knowledge(self, query: str) -> str:
        """Search knowledge base"""
        if not query:
            return "Please enter a search query"
        
        # Try to retrieve by key
        entry = self.orchestrator.retrieve_knowledge(query)
        if entry:
            return f"## Found: {query}\n\n```json\n{json.dumps(entry, indent=2, default=str)}\n```"
        
        return f"No knowledge found for: {query}"
    
    def create_ui(self):
        """Create the Gradio UI"""
        
        css = """
        .gradio-container {
            font-family: 'Inter', sans-serif;
        }
        .tab-nav button {
            font-size: 16px;
            font-weight: 500;
        }
        """
        
        with gr.Blocks(
            title="Master AI System",
            css=css,
            theme=gr.themes.Soft(primary_hue="blue")
        ) as ui:
            
            gr.Markdown("""
            # 🚀 Master AI System
            ### Unified Platform for Deep Research, Engineering, and Trading
            """)
            
            with gr.Tabs():
                
                # Dashboard Tab
                with gr.Tab("📊 Dashboard"):
                    gr.Markdown("## System Overview")
                    
                    with gr.Row():
                        status_display = gr.HTML(self.get_system_status())
                        refresh_btn = gr.Button("🔄 Refresh Status", size="sm")
                    
                    gr.Markdown("## Recent Events")
                    event_log_display = gr.HTML(self.get_event_log_html())
                    
                    # Auto-refresh every 5 seconds
                    refresh_btn.click(
                        fn=self.get_system_status,
                        outputs=status_display
                    )
                    
                    # Update event log
                    event_timer = gr.Timer(value=2)
                    event_timer.tick(
                        fn=self.get_event_log_html,
                        outputs=event_log_display
                    )
                
                # Deep Research Tab
                with gr.Tab("🔍 Deep Research"):
                    gr.Markdown("## Research Any Topic")
                    gr.Markdown("Enter a research query and get a comprehensive report with web search and analysis.")
                    
                    with gr.Row():
                        with gr.Column():
                            research_query = gr.Textbox(
                                label="Research Query",
                                placeholder="e.g., Latest developments in quantum computing",
                                lines=3
                            )
                            research_btn = gr.Button("🔍 Start Research", variant="primary")
                        
                        with gr.Column():
                            research_output = gr.Markdown(label="Research Results")
                    
                    research_btn.click(
                        fn=self.execute_research,
                        inputs=[research_query],
                        outputs=[research_output]
                    )
                
                # Engineering Team Tab
                with gr.Tab("⚙️ Engineering Team"):
                    gr.Markdown("## Build Custom Tools")
                    gr.Markdown("Describe what you want to build and the AI engineering team will create it.")
                    
                    with gr.Row():
                        with gr.Column():
                            engineering_requirements = gr.Textbox(
                                label="Requirements",
                                placeholder="Describe what you want to build...",
                                lines=5
                            )
                            engineering_module = gr.Textbox(
                                label="Module Name",
                                placeholder="module.py",
                                value="module.py"
                            )
                            engineering_btn = gr.Button("⚙️ Build Module", variant="primary")
                        
                        with gr.Column():
                            engineering_output = gr.Markdown(label="Build Results")
                    
                    engineering_btn.click(
                        fn=self.execute_engineering,
                        inputs=[engineering_requirements, engineering_module],
                        outputs=[engineering_output]
                    )
                
                # Trading Floor Tab
                with gr.Tab("💹 Trading Floor"):
                    gr.Markdown("## Portfolio Management")
                    gr.Markdown("View and manage AI trader portfolios.")
                    
                    gr.Markdown("### Coming Soon")
                    gr.Markdown("Integration with trading floor dashboard in progress...")
                
                # Workflows Tab
                with gr.Tab("🔄 Workflows"):
                    gr.Markdown("## Automated Workflows")
                    gr.Markdown("Execute predefined workflows that combine multiple systems.")
                    
                    with gr.Row():
                        with gr.Column():
                            workflow_type = gr.Dropdown(
                                label="Workflow Type",
                                choices=[
                                    "Research to Trade",
                                    "Build Tool",
                                    "Analyze Portfolio",
                                    "Market Research"
                                ],
                                value="Market Research"
                            )
                            workflow_params = gr.Textbox(
                                label="Parameters (JSON)",
                                placeholder='{"query": "AI trends", "trader_name": "Warren"}',
                                lines=5,
                                value='{"topics": ["AI stocks", "Tech trends"]}'
                            )
                            workflow_btn = gr.Button("▶️ Execute Workflow", variant="primary")
                        
                        with gr.Column():
                            workflow_output = gr.Markdown(label="Workflow Results")
                    
                    workflow_btn.click(
                        fn=self.execute_workflow,
                        inputs=[workflow_type, workflow_params],
                        outputs=[workflow_output]
                    )
                
                # Knowledge Base Tab
                with gr.Tab("🧠 Knowledge Base"):
                    gr.Markdown("## Shared Knowledge Graph")
                    gr.Markdown("Search and explore the shared knowledge base across all systems.")
                    
                    with gr.Row():
                        with gr.Column():
                            knowledge_query = gr.Textbox(
                                label="Search Query",
                                placeholder="Enter a key or topic to search..."
                            )
                            knowledge_btn = gr.Button("🔍 Search", variant="primary")
                        
                        with gr.Column():
                            knowledge_output = gr.Markdown(label="Search Results")
                    
                    knowledge_btn.click(
                        fn=self.search_knowledge,
                        inputs=[knowledge_query],
                        outputs=[knowledge_output]
                    )
                    
                    gr.Markdown("### Knowledge Statistics")
                    knowledge_stats = gr.HTML(
                        f"<p>Total entries: {len(self.orchestrator.knowledge_base)}</p>"
                    )
            
            gr.Markdown("""
            ---
            ### About
            This master application integrates three powerful AI systems:
            - **Deep Research**: Multi-agent research with web search and report generation
            - **Engineering Team**: Automated software development with CrewAI
            - **Trading Floor**: AI-powered portfolio management and trading
            
            All systems share a unified knowledge graph for cross-system learning and collaboration.
            """)
        
        return ui


def create_dashboard(orchestrator):
    """Create and return the dashboard UI"""
    dashboard = MasterDashboard(orchestrator)
    return dashboard.create_ui()
