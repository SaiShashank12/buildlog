"""
Tests for Analytics Service
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock
from app.services.analytics_service import AnalyticsService


class TestAnalyticsService:
    """Test suite for AnalyticsService"""

    @pytest.fixture
    def mock_appwrite(self):
        """Create mock Appwrite service"""
        mock = Mock()
        return mock

    @pytest.fixture
    def analytics_service(self, mock_appwrite):
        """Create AnalyticsService instance"""
        return AnalyticsService(mock_appwrite)

    @pytest.fixture
    def sample_projects(self):
        """Sample projects data"""
        return [
            {
                '$id': 'project1',
                'name': 'Test Project 1',
                'status': 'in_progress',
                'created_at': '2024-01-01T00:00:00'
            },
            {
                '$id': 'project2',
                'name': 'Test Project 2',
                'status': 'completed',
                'created_at': '2024-01-02T00:00:00'
            },
            {
                '$id': 'project3',
                'name': 'Test Project 3',
                'status': 'in_progress',
                'created_at': '2024-01-03T00:00:00'
            }
        ]

    @pytest.fixture
    def sample_logs(self):
        """Sample build logs data"""
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        return {
            'project1': [
                {
                    '$id': 'log1',
                    'title': 'First log',
                    'log_type': 'update',
                    'created_at': f'{today}T10:00:00'
                },
                {
                    '$id': 'log2',
                    'title': 'Second log',
                    'log_type': 'milestone',
                    'created_at': f'{yesterday}T10:00:00'
                }
            ],
            'project2': [
                {
                    '$id': 'log3',
                    'title': 'Third log',
                    'log_type': 'feature',
                    'created_at': f'{today}T11:00:00'
                }
            ],
            'project3': [
                {
                    '$id': 'log4',
                    'title': 'Fourth log',
                    'log_type': 'bug_fix',
                    'created_at': f'{week_ago}T10:00:00'
                }
            ]
        }

    def test_get_overview_stats(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting overview statistics"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        stats = analytics_service.get_overview_stats()

        assert stats['total_projects'] == 3
        assert stats['total_logs'] == 4
        assert stats['active_projects'] == 2
        assert stats['weekly_logs'] >= 0

    def test_get_overview_stats_empty(self, analytics_service, mock_appwrite):
        """Test getting overview stats with no data"""
        mock_appwrite.get_projects.return_value = []

        stats = analytics_service.get_overview_stats()

        assert stats['total_projects'] == 0
        assert stats['total_logs'] == 0
        assert stats['active_projects'] == 0
        assert stats['weekly_logs'] == 0

    def test_get_overview_stats_error_handling(self, analytics_service, mock_appwrite):
        """Test error handling in overview stats"""
        mock_appwrite.get_projects.side_effect = Exception("Database error")

        stats = analytics_service.get_overview_stats()

        assert stats['total_projects'] == 0
        assert stats['total_logs'] == 0

    def test_get_activity_over_time(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting activity over time"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        activity = analytics_service.get_activity_over_time(days=30)

        assert 'labels' in activity
        assert 'values' in activity
        assert len(activity['labels']) == 31  # 30 days + 1
        assert len(activity['values']) == 31

    def test_get_activity_over_time_custom_days(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting activity with custom day range"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        activity = analytics_service.get_activity_over_time(days=7)

        assert len(activity['labels']) == 8  # 7 days + 1
        assert len(activity['values']) == 8

    def test_get_log_type_distribution(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting log type distribution"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        distribution = analytics_service.get_log_type_distribution()

        assert 'labels' in distribution
        assert 'values' in distribution
        assert len(distribution['labels']) == len(distribution['values'])

        # Check that log types are formatted correctly
        assert all(isinstance(label, str) for label in distribution['labels'])
        assert sum(distribution['values']) == 4  # Total logs

    def test_get_log_type_distribution_empty(self, analytics_service, mock_appwrite):
        """Test log type distribution with no logs"""
        mock_appwrite.get_projects.return_value = []

        distribution = analytics_service.get_log_type_distribution()

        assert distribution['labels'] == []
        assert distribution['values'] == []

    def test_get_logs_per_project(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting logs per project"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        logs_per_project = analytics_service.get_logs_per_project()

        assert 'labels' in logs_per_project
        assert 'values' in logs_per_project
        assert len(logs_per_project['labels']) == 3
        assert len(logs_per_project['values']) == 3

        # Should be sorted by count (descending)
        assert logs_per_project['values'] == sorted(logs_per_project['values'], reverse=True)

    def test_get_logs_per_project_limit(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test logs per project with limit"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        logs_per_project = analytics_service.get_logs_per_project(limit=2)

        assert len(logs_per_project['labels']) == 2
        assert len(logs_per_project['values']) == 2

    def test_get_logs_per_project_truncate_names(self, analytics_service, mock_appwrite):
        """Test that long project names are truncated"""
        long_name_projects = [{
            '$id': 'project1',
            'name': 'A' * 50,  # Very long name
            'status': 'in_progress'
        }]

        mock_appwrite.get_projects.return_value = long_name_projects
        mock_appwrite.get_build_logs.return_value = [{'$id': 'log1'}]

        logs_per_project = analytics_service.get_logs_per_project()

        assert len(logs_per_project['labels'][0]) <= 20

    def test_get_weekly_trend(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting weekly trend"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        trend = analytics_service.get_weekly_trend(weeks=4)

        assert 'labels' in trend
        assert 'values' in trend
        assert len(trend['labels']) == 4
        assert len(trend['values']) == 4

    def test_get_weekly_trend_custom_weeks(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test weekly trend with custom week count"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        trend = analytics_service.get_weekly_trend(weeks=12)

        assert len(trend['labels']) == 12
        assert len(trend['values']) == 12

    def test_get_activity_heatmap(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting activity heatmap"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        heatmap = analytics_service.get_activity_heatmap(days=90)

        assert isinstance(heatmap, list)
        assert len(heatmap) == 91  # 90 days + 1

        # Check structure of heatmap data
        for day in heatmap:
            assert 'date' in day
            assert 'count' in day
            assert isinstance(day['count'], int)

    def test_get_activity_heatmap_custom_days(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test heatmap with custom day range"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        heatmap = analytics_service.get_activity_heatmap(days=30)

        assert len(heatmap) == 31

    def test_get_project_status_distribution(self, analytics_service, mock_appwrite, sample_projects):
        """Test getting project status distribution"""
        mock_appwrite.get_projects.return_value = sample_projects

        distribution = analytics_service.get_project_status_distribution()

        assert 'labels' in distribution
        assert 'values' in distribution
        assert len(distribution['labels']) == len(distribution['values'])

        # Check that statuses are formatted correctly
        assert all(isinstance(label, str) for label in distribution['labels'])

    def test_get_project_status_distribution_empty(self, analytics_service, mock_appwrite):
        """Test status distribution with no projects"""
        mock_appwrite.get_projects.return_value = []

        distribution = analytics_service.get_project_status_distribution()

        assert distribution['labels'] == []
        assert distribution['values'] == []

    def test_get_complete_analytics(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test getting complete analytics in one call"""
        mock_appwrite.get_projects.return_value = sample_projects
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        analytics = analytics_service.get_complete_analytics()

        # Check all required keys are present
        assert 'total_projects' in analytics
        assert 'total_logs' in analytics
        assert 'active_projects' in analytics
        assert 'weekly_logs' in analytics
        assert 'activity_over_time' in analytics
        assert 'log_type_distribution' in analytics
        assert 'logs_per_project' in analytics
        assert 'weekly_trend' in analytics
        assert 'project_status' in analytics

    def test_count_weekly_logs(self, analytics_service, mock_appwrite, sample_projects, sample_logs):
        """Test counting weekly logs"""
        mock_appwrite.get_build_logs.side_effect = lambda project_id: sample_logs.get(project_id, [])

        count = analytics_service._count_weekly_logs(sample_projects)

        assert isinstance(count, int)
        assert count >= 0

    def test_format_log_type(self, analytics_service):
        """Test log type formatting"""
        assert analytics_service._format_log_type('update') == 'Update'
        assert analytics_service._format_log_type('milestone') == 'Milestone'
        assert analytics_service._format_log_type('feature') == 'Feature'
        assert analytics_service._format_log_type('bug_fix') == 'Bug Fix'
        assert analytics_service._format_log_type('note') == 'Note'
        assert analytics_service._format_log_type('custom_type') == 'Custom Type'

    def test_error_handling_activity_over_time(self, analytics_service, mock_appwrite):
        """Test error handling in activity over time"""
        mock_appwrite.get_projects.side_effect = Exception("Network error")

        activity = analytics_service.get_activity_over_time()

        assert activity['labels'] == []
        assert activity['values'] == []

    def test_error_handling_weekly_trend(self, analytics_service, mock_appwrite):
        """Test error handling in weekly trend"""
        mock_appwrite.get_projects.side_effect = Exception("Network error")

        trend = analytics_service.get_weekly_trend()

        assert trend['labels'] == []
        assert trend['values'] == []

    def test_error_handling_heatmap(self, analytics_service, mock_appwrite):
        """Test error handling in heatmap"""
        mock_appwrite.get_projects.side_effect = Exception("Network error")

        heatmap = analytics_service.get_activity_heatmap()

        assert heatmap == []
