from manim import *
from manim.utils.rate_functions import *
class AnimateParabola(Scene):
    def construct(self):
        # Constants
        b = 50
        c = 100
        x_range = (0, 100, 1)  # x values from 0 to 100
        a_values = [0.05]  # Different values for a
        a_values.extend(a_values[-1] + 0.05 * i for i in range(1, 10))
        graphs = []
        # Axes setup
        axes = Axes(
            x_range=[0, 100, 10],
            y_range=[0, 150, 10],  # y range starts from 0
            axis_config={"color": WHITE},
            x_length=10,
            y_length=6,
            x_axis_config={"numbers_to_include": [0, 20, 40, b, 60, 80, 100]},  # Display specific x-axis values
            y_axis_config={"numbers_to_include": [0, 50, 100, 150]}  # Display specific y-axis values
        ).to_edge(DOWN)

        axes_labels = axes.get_axis_labels(x_label="x", y_label="F(x)")

        # Create the initial graph for the first a value
        def parabola(x, a):
            return -a * (x - b) ** 2 + c

        # Create the optimal level line at y = b using DashedLine
        optimal_line = DashedLine(
            start=axes.c2p(b, 0), 
            end=axes.c2p(b, c),  
            color=YELLOW, 
            stroke_width=2
        )
        optimal_label = MathTex("y = b").next_to(optimal_line, DOWN).shift(DOWN)

        # Create the initial graph for the first value of a
        graph = axes.plot(lambda x: parabola(x, a_values[0]), x_range=x_range, color=BLUE)
        graph_label = axes.get_graph_label(graph)

        # Add the initial label for 'a' above the graph
        a_label = MathTex(f"a = {a_values[0]:.2f}")
        a_label.next_to(graph, UP)
        
        # Create the scene
        self.play(Create(axes), Write(axes_labels), run_time = 1, rate_func=linear)
        
        self.play(Create(graph), Write(graph_label), Write(a_label), run_time = 1.5)
        
        self.play(Create(optimal_line), Write(optimal_label), run_time = 1.5)

        # Create an arrow pointing to the yellow dashed line
        arrow = Arrow(
            start=axes.c2p(90, 70),  # starting point of the arrow
            end=axes.c2p(b, 50),  # ending point of the arrow (pointing to the line)
            color=WHITE,
            buff=0.1
        )
        arrow_label = MathTex("y = b").next_to(arrow, RIGHT).shift(UP * 0.5)

        # Animate the arrow pointing to the dashed line
        self.play(Create(arrow), Write(arrow_label))

        # Update graph with new values of a
        for a in a_values[1:]:
            new_graph = axes.plot(lambda x: parabola(x, a), x_range=x_range, color=BLUE)
            new_graph_label = axes.get_graph_label(new_graph)

            # Create a new label for 'a'
            new_a_label = MathTex(f"a = {a:.2f}")
            new_a_label.next_to(new_graph, UP)
            if a_values.index(a) <= len(a_values)//3:
                run_time = 3
            # Animating the transition faster with run_time=1
            elif a_values.index(a) > len(a_values)//3 and a_values.index(a) <= len(a_values)//2:
                run_time = 2
            else:
                run_time = 1  
            self.play(
                Transform(graph, new_graph),
                Transform(graph_label, new_graph_label),
                Transform(a_label, new_a_label),
                run_time=run_time,
                rate_func=double_smooth,
            )

        self.play(FadeOut(arrow), FadeOut(arrow_label))

        self.wait(1)

        graph_1 = axes.plot(lambda x: parabola(x, a_values[1]), x_range=x_range, color=BLUE)
        graph_1_label = axes.get_graph_label(graph_1)

        
        
        arrow_1 = Arrow(
            start=axes.c2p(10, 70),  # starting point of the arrow
            end=axes.c2p(30, parabola(30, a_values[1])),  # ending point of the arrow (pointing to the line)
            color=GREEN,
            buff=0.1
        )
        arrow_1_label = MathTex(f"a = {a_values[1]:.2f}", color=GREEN).next_to(arrow_1, LEFT).shift(UP * 0.5).shift(RIGHT * 1)
        
        
        new_graph_1 = axes.plot(lambda x: parabola(x, a_values[1]), x_range=x_range, color=GREEN)
        
        
        graph = axes.plot(lambda x: parabola(x, a_values[4]), x_range=x_range, color=BLUE)
        graph_label = axes.get_graph_label(graph)


        arrow_2 = Arrow(
            start=axes.c2p(90, 70),  # starting point of the arrow
            end=axes.c2p(60, parabola(60, a_values[4])),  # ending point of the arrow (pointing to the line)
            color=PINK,
            buff=0.1
        )
        arrow_2_label = MathTex(f"a = {a_values[4]:.2f}", color=PINK).next_to(arrow, RIGHT).shift(UP * 0.5)


        
        new_graph_2 = axes.plot(lambda x: parabola(x, a_values[4]), x_range=x_range, color=PINK)
        
        self.play(Create(graph_1), Write(graph_1_label), Create(graph), Write(graph_label), Write(a_label), run_time = 4)
        
        self.play(Transform(graph_1, new_graph_1), Transform(graph, new_graph_2), run_time = 1.5)
        
        
        self.play(Create(arrow_2), Write(arrow_2_label), Create(arrow_1), Write(arrow_1_label), run_time = 1.5)
        
        self.wait(1)

