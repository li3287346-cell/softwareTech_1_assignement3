from src.services.workflow_service import WorkflowService
from src.app import MacroApp


def main() -> None:
    """Run Stage 1 then launch the EDA viewer GUI."""
    workflow = WorkflowService()
    workflow.run_full_pipeline()

    app = MacroApp()
    app.mainloop()


if __name__ == "__main__":
    main()
