import streamlit as st
st.page_link("./titanic.py", label="Try Again", icon="🚢")
# Function to create vertical falling balls
def confetti():
    # HTML, CSS, and JavaScript for vertical falling balls
    confetti_html = """
    <p id="congrats">Congrats! You survived the Titanic.</p>
    <div id="confetti-container"</div>

    <style>
    /* Confetti container */
    #confetti-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 9999;
    }
    #congrats{
        position: relative;
        top: 100px;
        color: white;
    }

    /* Individual confetti balls */
    .ball {
        position: absolute;
        width: 12px;
        height: 12px;
        background-color: var(--ball-color, #aaa); /* Default muted color */
        border-radius: 50%;
        animation: fall 5s linear infinite;
    }

    /* Falling animation (y-axis only) */
    @keyframes fall {
        0% {
            transform: translateY(-70%); /* Start slightly above the screen */
        }
        100% {
            transform: translateY(2700%); /* End slightly below the screen */
        }
    }
    </style>

    <script>
    function generateBalls() {
        const mutedColors = ['#4C5B5C', '#FF715B', '#F9CB40', '#BCED09', '#DE8F6E', '#DBD56E', '#88AB75'];
        const container = document.getElementById("confetti-container");

        for (let i = 0; i < 70; i++) {
            // Create a ball
            const ball = document.createElement("div");
            ball.classList.add("ball");
            ball.style.setProperty("--ball-color", mutedColors[Math.floor(Math.random() * mutedColors.length)]);
            ball.style.left = Math.random() * 100 + "vw"; // Random horizontal position
            ball.style.animationDelay = Math.random() * 2 + "s"; // Random start time
            ball.style.animationDuration = (Math.random() * 2 + 3) + "s"; // Vary falling speed
            container.appendChild(ball);
        }

        // Clear balls after 3 seconds
        setTimeout(() => {
            container.innerHTML = "";
        }, 5000);
    }

    // Trigger the ball animation
    generateBalls();
    </script>
    """

    # Embed the HTML and animation in the Streamlit app
    st.components.v1.html(confetti_html, height=700)

confetti()
st.balloons()


