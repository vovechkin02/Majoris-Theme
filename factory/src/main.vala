namespace MajorisThemeFactory {
    public int main (string[] args) {
        bool geometry = false;
        string page="overview";
        string variant="light";
        foreach (var arg in args) {
            if (arg == "--geometry-report") geometry = true;
            if(arg.has_prefix("--page=")) page=arg.substring(7);
            if(arg=="--light" || arg=="--dark" || arg=="--system") variant=arg.substring(2);
        }
        var app = new Application (geometry,page,variant);
        return app.run ({ args[0] });
    }
}
