class Navigation:
    def __init__(self):
        self.active_view = None

    def switch_view(self, view_name):
        self.active_view = view_name
        self.update_navigation_state()

    def update_navigation_state(self):
        # Logic to update the navigation UI based on the active view
        pass

    def get_active_view(self):
        return self.active_view