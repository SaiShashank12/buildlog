"""
Analytics service for calculating project and build log statistics
"""
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any


class AnalyticsService:
    """Service for generating analytics and statistics"""

    def __init__(self, appwrite_service):
        self.appwrite = appwrite_service

    def get_overview_stats(self, user_id: str = "demo_user") -> Dict[str, int]:
        """Get overview statistics"""
        try:
            # Get all projects
            projects = self.appwrite.get_projects(user_id)
            total_projects = len(projects)

            # Count active projects
            active_projects = sum(1 for p in projects if p.get('status') == 'in_progress')

            # Get all build logs
            total_logs = 0
            for project in projects:
                logs = self.appwrite.get_build_logs(project['$id'])
                total_logs += len(logs)

            # Calculate weekly logs
            weekly_logs = self._count_weekly_logs(projects)

            return {
                'total_projects': total_projects,
                'total_logs': total_logs,
                'active_projects': active_projects,
                'weekly_logs': weekly_logs
            }
        except Exception as e:
            print(f"Error getting overview stats: {e}")
            return {
                'total_projects': 0,
                'total_logs': 0,
                'active_projects': 0,
                'weekly_logs': 0
            }

    def get_activity_over_time(self, user_id: str = "demo_user", days: int = 30) -> Dict[str, List]:
        """Get activity over the last N days"""
        try:
            projects = self.appwrite.get_projects(user_id)

            # Initialize date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Create date labels
            dates = []
            current = start_date
            while current <= end_date:
                dates.append(current.strftime('%Y-%m-%d'))
                current += timedelta(days=1)

            # Count logs per day
            activity_by_date = defaultdict(int)

            for project in projects:
                logs = self.appwrite.get_build_logs(project['$id'])
                for log in logs:
                    log_date = log.get('created_at', '')[:10]  # Get YYYY-MM-DD
                    if log_date in dates:
                        activity_by_date[log_date] += 1

            # Create values list matching dates
            values = [activity_by_date.get(date, 0) for date in dates]

            # Format labels (show every 5 days for readability)
            labels = []
            for i, date in enumerate(dates):
                if i % 5 == 0 or i == len(dates) - 1:
                    dt = datetime.strptime(date, '%Y-%m-%d')
                    labels.append(dt.strftime('%b %d'))
                else:
                    labels.append('')

            return {
                'labels': labels,
                'values': values
            }
        except Exception as e:
            print(f"Error getting activity over time: {e}")
            return {'labels': [], 'values': []}

    def get_log_type_distribution(self, user_id: str = "demo_user") -> Dict[str, List]:
        """Get distribution of log types"""
        try:
            projects = self.appwrite.get_projects(user_id)
            log_types = defaultdict(int)

            for project in projects:
                logs = self.appwrite.get_build_logs(project['$id'])
                for log in logs:
                    log_type = log.get('log_type', 'note')
                    log_types[log_type] += 1

            # Sort by count
            sorted_types = sorted(log_types.items(), key=lambda x: x[1], reverse=True)

            labels = [self._format_log_type(t[0]) for t in sorted_types]
            values = [t[1] for t in sorted_types]

            return {
                'labels': labels,
                'values': values
            }
        except Exception as e:
            print(f"Error getting log type distribution: {e}")
            return {'labels': [], 'values': []}

    def get_logs_per_project(self, user_id: str = "demo_user", limit: int = 10) -> Dict[str, List]:
        """Get number of logs per project"""
        try:
            projects = self.appwrite.get_projects(user_id)
            project_logs = []

            for project in projects:
                logs = self.appwrite.get_build_logs(project['$id'])
                project_logs.append({
                    'name': project.get('name', 'Untitled'),
                    'count': len(logs)
                })

            # Sort by count and limit
            project_logs.sort(key=lambda x: x['count'], reverse=True)
            project_logs = project_logs[:limit]

            labels = [p['name'][:20] for p in project_logs]  # Truncate long names
            values = [p['count'] for p in project_logs]

            return {
                'labels': labels,
                'values': values
            }
        except Exception as e:
            print(f"Error getting logs per project: {e}")
            return {'labels': [], 'values': []}

    def get_weekly_trend(self, user_id: str = "demo_user", weeks: int = 8) -> Dict[str, List]:
        """Get weekly activity trend"""
        try:
            projects = self.appwrite.get_projects(user_id)

            # Calculate week ranges
            end_date = datetime.now()
            week_data = []

            for i in range(weeks - 1, -1, -1):
                week_start = end_date - timedelta(weeks=i, days=end_date.weekday())
                week_end = week_start + timedelta(days=6)
                week_data.append({
                    'start': week_start.strftime('%Y-%m-%d'),
                    'end': week_end.strftime('%Y-%m-%d'),
                    'label': week_start.strftime('%b %d'),
                    'count': 0
                })

            # Count logs per week
            for project in projects:
                logs = self.appwrite.get_build_logs(project['$id'])
                for log in logs:
                    log_date = log.get('created_at', '')[:10]
                    for week in week_data:
                        if week['start'] <= log_date <= week['end']:
                            week['count'] += 1
                            break

            labels = [w['label'] for w in week_data]
            values = [w['count'] for w in week_data]

            return {
                'labels': labels,
                'values': values
            }
        except Exception as e:
            print(f"Error getting weekly trend: {e}")
            return {'labels': [], 'values': []}

    def get_activity_heatmap(self, user_id: str = "demo_user", days: int = 365) -> List[Dict]:
        """Get activity heatmap data (GitHub-style) - 12 months"""
        try:
            projects = self.appwrite.get_projects(user_id)

            # Initialize date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Count logs per day
            activity_by_date = defaultdict(int)

            for project in projects:
                logs = self.appwrite.get_build_logs(project['$id'])
                for log in logs:
                    log_date = log.get('created_at', '')[:10]
                    activity_by_date[log_date] += 1

            # Create heatmap data
            heatmap_data = []
            current = start_date
            while current <= end_date:
                date_str = current.strftime('%Y-%m-%d')
                heatmap_data.append({
                    'date': date_str,
                    'count': activity_by_date.get(date_str, 0)
                })
                current += timedelta(days=1)

            return heatmap_data
        except Exception as e:
            print(f"Error getting activity heatmap: {e}")
            return []

    def get_project_status_distribution(self, user_id: str = "demo_user") -> Dict[str, List]:
        """Get distribution of project statuses"""
        try:
            projects = self.appwrite.get_projects(user_id)
            status_counts = defaultdict(int)

            for project in projects:
                status = project.get('status', 'in_progress')
                status_counts[status] += 1

            # Map status to readable labels
            status_map = {
                'in_progress': 'In Progress',
                'completed': 'Completed',
                'archived': 'Archived'
            }

            labels = [status_map.get(s, s.title()) for s in status_counts.keys()]
            values = list(status_counts.values())

            return {
                'labels': labels,
                'values': values
            }
        except Exception as e:
            print(f"Error getting project status distribution: {e}")
            return {'labels': [], 'values': []}

    def get_complete_analytics(self, user_id: str = "demo_user") -> Dict[str, Any]:
        """Get all analytics data in one call"""
        return {
            **self.get_overview_stats(user_id),
            'activity_over_time': self.get_activity_over_time(user_id),
            'log_type_distribution': self.get_log_type_distribution(user_id),
            'logs_per_project': self.get_logs_per_project(user_id),
            'weekly_trend': self.get_weekly_trend(user_id),
            'project_status': self.get_project_status_distribution(user_id)
        }

    def _count_weekly_logs(self, projects: List[Dict]) -> int:
        """Count logs from the past 7 days"""
        try:
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            count = 0

            for project in projects:
                logs = self.appwrite.get_build_logs(project['$id'])
                for log in logs:
                    log_date = log.get('created_at', '')[:10]
                    if log_date >= week_ago:
                        count += 1

            return count
        except Exception as e:
            print(f"Error counting weekly logs: {e}")
            return 0

    def _format_log_type(self, log_type: str) -> str:
        """Format log type for display"""
        type_map = {
            'update': 'Update',
            'milestone': 'Milestone',
            'feature': 'Feature',
            'bug_fix': 'Bug Fix',
            'note': 'Note'
        }
        return type_map.get(log_type, log_type.replace('_', ' ').title())
