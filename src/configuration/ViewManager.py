class ViewManager:
    def __new__(viewManager):
        if not hasattr(viewManager, 'instance'):
            viewManager.instance = super(viewManager, viewManager).__new__(viewManager)
        return viewManager.instance

    def __init__(self):
        self.viewManager = {}

    def get(self, viewName):
        return self.viewManager[viewName]
    
    def registerView(self, viewName, view):
        # TODO check if view passed is instance of SMSView
        if viewName not in self.viewManager:
            self.viewManager[viewName] = view

    def unregisterView(self, viewName):
        del self.viewManager[viewName]

    def registerViews(self, views):
        for viewName, view in views.items():
            self.registerView(viewName, view)