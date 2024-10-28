import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget, render_plotly
import seaborn as sns
from shiny import render 


penguins = load_penguins()

ui.page_opts(title="Andrea's Penguin Playground", fillable=False)

with ui.sidebar(open="open"):
    ui.h2("Sidebar")

    ui.input_selectize("selected_attribute","Select Attributes",
                       ["bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"])
    
    ui.input_numeric("plotly_bin_count","Ploty Bins",1,min=1,max=20)
    ui.input_slider("seaborn_bin_count","Seaborn Bins",1,20,10)
    ui.input_checkbox_group("selected_species_list","Choose Species",
                           ["Adelie", "Gentoo","Chinstrap"],
                           selected=["Adelie","Gentoo"],
                           inline=False)
    ui.hr()
    ui.a("Andrea's Github",href="https://github.com/andrea-shobe", target="_blank")


with ui.layout_columns():
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def penguinstable_df():
            return render.DataTable(penguins, filters=True,selection_mode='row')
        

    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def penguinsgrid_df():
            return render.DataGrid(penguins, filters=True, selection_mode="row")


with ui.layout_columns():
    with ui.card():
        @render.plot(alt="A Seaborn Histogram")
        def plot():
            ax=sns.histplot(data=penguins,x="body_mass_g",bins=input.seaborn_bin_count())
            ax.set_title("Palmer Penguins")
            ax.set_xlabel("Mass (g)")
            ax.set_ylabel("Count")
            return ax
            
    with ui.card():
        "Plotly Histogram"
        @render_plotly
        def plotlyhistogram():
            return px.histogram(penguins,x=input.selected_attribute(),
                               nbins=input.plotly_bin_count(), color="species").update_layout(
                xaxis_title="Bill Length (mm)",
                yaxis_title="Count",)

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            data_frame=penguins,
            x="body_mass_g",
            y="bill_depth_mm",
            color="species",
            color_discrete_sequence=["red","orange","blue"],
            labels={"body_mass_g": "Body Mass (g)",
                   "bill_depth_mm":"Bil Depth (mm):"})
        
