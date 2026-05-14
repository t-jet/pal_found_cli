"""Tests for adhoc-modifications-04 requirements: enhanced list and build-queue commands."""

from pathlib import Path
import pytest
from tracker.links import is_ticket_blocked, create_link
from tracker.tickets import list_tickets, create_ticket
from tests.conftest import run_main


class TestListEnhancements:
    """Test enhanced list command features."""
    
    def test_list_includes_reporter_column(self, tracker_env: Path):
        """Test that list command includes reporter column."""
        # Create a ticket
        create_ticket("task", "Test Task", "john-doe", priority="High", assignee="jane-doe")
        
        # Run list command
        output, exit_code = run_main(["list"])
        
        assert "Reporter" in output
        assert "john-doe" in output
    
    def test_list_includes_blocked_status(self, tracker_env: Path):
        """Test that list command shows blocked status."""
        # Create two tickets
        ticket1 = create_ticket("task", "Task 1", "author", priority="High", assignee="dev1")
        ticket2 = create_ticket("task", "Task 2", "author", priority="Medium", assignee="dev2")
        
        # Create blocking link
        create_link(ticket1, ticket2, "Blocks", "author")
        
        # Run list command
        output, exit_code = run_main(["list"])
        
        assert "Blocked" in output
        assert "Yes" in output or "No" in output
    
    def test_list_multi_value_status_filter(self, tracker_env: Path):
        """Test list command with multiple status values (OR logic)."""
        # Create tickets with different statuses
        create_ticket("task", "Task 1", "author", priority="High", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="High", assignee="dev2")
        
        # Test that multiple status values can be passed
        output, exit_code = run_main(["list", "--status", "New", "--status", "Open"])
        
        # Should not error
        assert exit_code == 0
    
    def test_list_multi_value_type_filter(self, tracker_env: Path):
        """Test list command with multiple type values (OR logic)."""
        # Create tickets of different types
        create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        create_ticket("workitem", "Work 1", "author", parent="")
        
        # Filter for task and workitem
        output, exit_code = run_main(["list", "--type", "task", "--type", "workitem"])
        
        assert exit_code == 0
    
    def test_list_multi_value_priority_filter(self, tracker_env: Path):
        """Test list command with multiple priority values (OR logic)."""
        create_ticket("task", "Task 1", "author", priority="Low", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="High", assignee="dev2")
        create_ticket("task", "Task 3", "author", priority="Critical", assignee="dev3")
        
        # Filter for High and Critical
        output, exit_code = run_main(["list", "--priority", "High", "--priority", "Critical"])
        
        assert exit_code == 0
        # Verify the filtering worked
        assert "Task 2" in output or "Task 3" in output
    
    def test_list_non_terminal_only(self, tracker_env: Path):
        """Test list command with --non-terminal-only flag."""
        # Create tickets (all will be in "New" status which is non-terminal)
        create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="High", assignee="dev2")
        
        # Run with non-terminal-only flag
        output, exit_code = run_main(["list", "--non-terminal-only"])
        
        assert exit_code == 0


class TestListTicketsFunction:
    """Test the enhanced list_tickets function directly."""
    
    def test_list_tickets_multi_value_status(self, tracker_env: Path):
        """Test list_tickets with list of statuses."""
        create_ticket("task", "Task 1", "author", priority="High", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="Medium", assignee="dev2")
        
        # Test with list of statuses
        tickets = list_tickets(status=["New"])
        assert len(tickets) >= 2
        
        # Test with single status (backwards compatible)
        tickets = list_tickets(status="New")
        assert len(tickets) >= 2
    
    def test_list_tickets_multi_value_type(self, tracker_env: Path):
        """Test list_tickets with list of types."""
        create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        
        # Filter for task
        tickets = list_tickets(ticket_type=["task"])
        assert len(tickets) >= 1
        
        # Verify only tasks returned
        for t in tickets:
            assert t["type"] == "task"
    
    def test_list_tickets_multi_value_priority(self, tracker_env: Path):
        """Test list_tickets with list of priorities."""
        create_ticket("task", "Task Low", "author", priority="Low", assignee="dev1")
        create_ticket("task", "Task High", "author", priority="High", assignee="dev2")
        create_ticket("task", "Task Critical", "author", priority="Critical", assignee="dev3")
        
        # Filter for High and Critical
        tickets = list_tickets(priority=["High", "Critical"])
        assert len(tickets) == 2
        
        priorities = [t["priority"] for t in tickets]
        assert "Low" not in priorities
    
    def test_list_tickets_non_terminal_only(self, tracker_env: Path):
        """Test list_tickets with non_terminal_only flag."""
        # Create some tickets (all in New status, which is non-terminal)
        create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="High", assignee="dev2")
        
        tickets = list_tickets(non_terminal_only=True)
        assert len(tickets) >= 2
        
        # Verify all tickets are indeed non-terminal
        from tracker.config import get_runtime_config
        cfg = get_runtime_config()
        for ticket in tickets:
            terminal_statuses = cfg["ticket_specs"][ticket["type"]].get("terminal_statuses", [])
            assert ticket["status"] not in terminal_statuses


class TestIsTicketBlocked:
    """Test the is_ticket_blocked function."""
    
    def test_ticket_not_blocked(self, tracker_env: Path):
        """Test that a ticket without blocking links is not blocked."""
        ticket_id = create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        assert not is_ticket_blocked(ticket_id)
    
    def test_ticket_blocked_by_blocks_link(self, tracker_env: Path):
        """Test that a ticket is blocked when targeted by a Blocks link."""
        ticket1 = create_ticket("task", "Task 1", "author", priority="High", assignee="dev1")
        ticket2 = create_ticket("task", "Task 2", "author", priority="Medium", assignee="dev2")
        
        # ticket1 blocks ticket2
        create_link(ticket1, ticket2, "Blocks", "author")
        
        # ticket2 should be blocked
        assert is_ticket_blocked(ticket2)
        # ticket1 should not be blocked
        assert not is_ticket_blocked(ticket1)
    
    def test_ticket_not_blocked_by_non_blocking_link(self, tracker_env: Path):
        """Test that non-blocking link types don't block tickets."""
        ticket1 = create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        ticket2 = create_ticket("task", "Task 2", "author", priority="High", assignee="dev2")
        
        # Create a RelatesTo link (not blocking)
        create_link(ticket1, ticket2, "RelatesTo", "author")
        
        # Neither should be blocked
        assert not is_ticket_blocked(ticket1)
        assert not is_ticket_blocked(ticket2)


class TestBuildQueueCommand:
    """Test build-queue command."""
    
    def test_build_queue_stage1(self, tracker_env: Path):
        """Test build-queue stage1 (filter non-terminal tickets)."""
        create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="High", assignee="dev2")
        
        output, exit_code = run_main(["build-queue", "stage1"])
        
        assert exit_code == 0
    
    def test_build_queue_stage2(self, tracker_env: Path):
        """Test build-queue stage2 (priority cleanup)."""
        create_ticket("task", "Task 1", "author", priority="High", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="Low", assignee="dev2")
        
        output, exit_code = run_main(["build-queue", "stage2", "--author", "system"])
        
        assert exit_code == 0
    
    def test_build_queue_stage3(self, tracker_env: Path):
        """Test build-queue stage3 (sort queue)."""
        create_ticket("task", "Task 1", "author", priority="Medium", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="Critical", assignee="dev2")
        
        output, exit_code = run_main(["build-queue", "stage3"])
        
        assert exit_code == 0
    
    def test_build_queue_stage4(self, tracker_env: Path):
        """Test build-queue stage4 (output)."""
        create_ticket("task", "Task 1", "author", priority="High", assignee="dev1")
        
        output, exit_code = run_main(["build-queue", "stage4"])
        
        assert exit_code == 0
    
    def test_build_queue_all(self, tracker_env: Path):
        """Test build-queue all (run all stages)."""
        create_ticket("task", "Task 1", "author", priority="Critical", assignee="dev1")
        create_ticket("task", "Task 2", "author", priority="High", assignee="dev2")
        create_ticket("task", "Task 3", "author", priority="Medium", assignee="dev3")
        
        output, exit_code = run_main(["build-queue", "all", "--author", "system"])
        
        assert exit_code == 0
        assert "Stage 1" in output
        assert "Stage 2" in output
        assert "Stage 3" in output
        assert "Stage 4" in output


class TestConfigEnhancements:
    """Test configuration enhancements for blocking links."""
    
    def test_link_blocking_in_runtime_config(self, tracker_env: Path):
        """Test that link_blocking is populated in runtime config."""
        from tracker.config import get_runtime_config
        
        cfg = get_runtime_config()
        assert "link_blocking" in cfg
        assert cfg["link_blocking"]["Blocks"] is True
        assert cfg["link_blocking"].get("RelatesTo", False) is False
