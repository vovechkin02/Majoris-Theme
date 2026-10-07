namespace MajorisThemeFactory {
    public int main (string[] args) {
        bool geometry = false;
        foreach (var arg in args) if (arg == "--geometry-report") geometry = true;
        var app = new Application (geometry);
        return app.run ({ args[0] });
    }
}
