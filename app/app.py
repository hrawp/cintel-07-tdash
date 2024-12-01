import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

df = palmerpenguins.load_penguins()

ui.page_opts(title="Aaron's Penguins Dashboard", fillable=True)


with ui.sidebar(title="Filtering Data Controls"):
    #This first input on the sidebar is to filter results by the mass of the penguins.
    #This has an upper bound of 6000, and lower bound of 2000.
    #This also sets to default to 6000.
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links to the Project")
    #The links below are also in the sidebar.  This are links to different parts
    #of the project details and reside in GitHub.  I updated these to poin
    #to my GitHub artifacts. 
    ui.a(
        "GitHub Source",
        href="https://github.com/hrawp/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/hrawp/cintel-07-tdash/blob/main/app/app.py",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/hrawp/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False):
    #The following line imports and image of a bird. You have to have
    #faicons installed and then imported for this to work.
    with ui.value_box(showcase=icon_svg("earlybirds")):
        #theme="bg-gradient-red-orange"
        "Number of Penguins"
    #@render.text is for positioning text in a value box.  
        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill Length and Depth")
        #This is for plotting data in a scatterplot.  We define what
        #the x and y corridante data should be displayed with the 
        #data in the data frame.
        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")
        #This allows us to put data in a table or Data Grid.  Again it 
        #uses a data frame.
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


@reactive.calc
#This is the reactive.calc for this app.
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df