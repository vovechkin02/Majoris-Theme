# Files spacing inventory

Read-only audit of the sibling `Majoris-Files` checkout on 2026-11-01. Files was
not modified. Allocation values below come from equivalent native Theme fixtures;
they are not measurements of a running Files process. Backend/service dependent
Files dialogs were substituted with the relevant native widget hierarchy.

| Source / parent | Children and explicit geometry | Existing Theme ownership | Expected / measured | Classification |
|---|---|---|---|---|
| `metadata/tags-dialog.vala`, TagsDialog PreferencesGroup | SearchEntry, boxed ListBox, hidden TagNameEditor (internal spacing 4), horizontal controls spacing 8; content width 420; no inter-control margins | Previously group heading gap only; new internal content-box gap | Search/list 8; list/actions 8; revealed editor 8 on each side; buttons 8 | Automatically covered |
| Same file, ManageTagsDialog PreferencesGroup | ListBox then Rename/Delete box spacing 8; width 560; heading New button | New internal content-box gap; row contract unchanged | List/actions 8, buttons 8 | Automatically covered |
| Same file, TagPalette | Popover / vertical Box spacing 8 / neutral FlowBox and custom button | Outer popover padding 8; no new anonymous-box spacing | Existing explicit 8 retained; palette tile geometry app-defined | Already conforming / intentionally application-defined |
| Same file, TagManageRow | ListBoxRow / horizontal Box spacing 12 / color MenuButton, name Stack, Switch | Existing row geometry | 12 within custom identity row preserved; no new descendant gaps | Intentionally application-defined |
| `dialogs/split.vala`, SplitDialog | PreferencesDialog / Page / Group / ActionRows, ComboRows, SwitchRow; final standalone suggested Button | Boxed-list internals continuous; new group content gap | Internal rows 0 between boundaries; list/button 8 | Automatically covered |
| `sharing/settings.vala`, SharingPage | Groups of native rows plus Reload button; apply/stop horizontal Box spacing 8 | Group content gap; 16 between page groups | 8 from row-list to standalone controls; 8 within explicit button box retained | Automatically covered |
| Same file, account actions | Horizontal Box spacing 4 in account interface | No new anonymous-box override | Existing compact 4 retained | Intentionally application-defined |
| `search/filters.vala` | PreferencesPage / Groups / EntryRows, ComboRows, SwitchRows; separate actions Group with horizontal Box spacing 8 | Existing page 16, row geometry; new content spacing does not insert row gaps | Existing 16 group gap, action buttons 8 | Already conforming |
| `dialogs/properties.vala` | PreferencesDialog / Page / Groups; identity horizontal Box spacing 12; tag markers spacing 4; ActionRow suffix value labels | Existing heading, label and suffix rules unchanged | Identity 12 and marker 4 retained; ActionRows unchanged in existing regression tests | Intentionally application-defined / already conforming |
| `chooser/window.vala` | Vertical root Box spacing 8; footer horizontal Box spacing 8, margins start/end/bottom 12, top 8; summary margins start/end 12; choice rows spacing 8 | No native footer CSS identifier | Explicit app geometry preserved; cannot impose a 16px inset safely by inferring role from orientation | Semantic contract required for future standard inset/footer adoption |
| `window/window.vala`, operations | Popover / vertical Box spacing 6 / label, ProgressBar, Cancel; progress at 180px | Popover inset only; no anonymous-box override | Existing 6 preserved; intended semantic progress uses 8 title/bar, 4 bar/support, 8 actions | Semantic contract required |
| `views/browser.vala` | Browser vertical Box spacing 0; structural grids; address fields column-spacing 8 | Phase 2 SearchBar, toolbar/location and data views own their geometry | Structural 0 preserved; field columns 8 preserved | Intentionally application-defined |
| Search/results within PreferencesGroup | SearchEntry and results ListBox | New content box rule | Actual 8 | Automatically covered |
| Anonymous search/filter Box outside a recognised group | Role and spacing property cannot be selected from CSS | No broad rule | Use zero-spacing `majoris-control-stack` / `majoris-field` as appropriate | Semantic contract required |

No source-only case above is represented as a measured Files allocation. Native
measurement JSON gives complete boundaries and property values for the Theme
fixtures. Existing dedicated factory regressions supply toolbar, sidebar,
breadcrumb, property-row and data-view evidence independently of Files services.
