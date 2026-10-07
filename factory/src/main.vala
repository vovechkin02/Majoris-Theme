namespace MajorisThemeFactory {
    public int main (string[] args) {
        bool geometry = false;
        string page="overview";
        foreach (var arg in args) {
            if (arg == "--geometry-report") geometry = true;
            if(arg.has_prefix("--page=")) page=arg.substring(7);
        }
        var app = new Application (geometry,page);
        return app.run ({ args[0] });
    }
}
