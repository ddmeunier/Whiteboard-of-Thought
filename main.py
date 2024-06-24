from openai import OpenAI   
import turtle
import os
from config import Config
import subprocess
import base64

def check_ghostscript():
    try:
        output = subprocess.check_output(['gswin64c', '-version'], stderr=subprocess.STDOUT)
        print("Ghostscript found:", output)
    except subprocess.CalledProcessError as e:
        print("Ghostscript error:", e.output)
    except FileNotFoundError:
        print("Ghostscript is not installed or not found in PATH.")


def draw_q():
    # Set up the turtle environment
    screen = turtle.Screen()
    screen.setup(width=200, height=200)
    screen.bgcolor("white")

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(1)

    # Draw the circle
    pen.penup()
    pen.goto(0, -50)
    pen.pendown()
    pen.circle(50)

    # Draw the vertical line
    pen.penup()
    pen.goto(50, 0)
    pen.pendown()
    pen.goto(50, -100)

    # Save the drawing to a file
    ts = turtle.getcanvas()
    ts.postscript(file="q_letter.eps")

    # Close the turtle screen
    turtle.bye()

def identify_letter_from_image():
    # Convert the EPS file to PNG or any other format OpenAI can use (if needed)
    # This requires installing an external tool like ImageMagick or PIL
    from PIL import Image
    img = Image.open("q_letter.eps")
    img.save("q_letter.png", "png")

    # Initialize OpenAI instance
    openai_client = OpenAI(api_key=Config.OPENAI_API)
    # Describe the image to OpenAI
    description = "The image shows a circle with a vertical line touching it to the right going down."
    with open("q_letter.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    response = openai_client.chat.completions.create(
        model=Config.CURRENT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant and an expert at paying close attention to image details. You are also an expert at identifying letters from the English alphabet."},
            {"role": "user", 
             "content": [
                {"type": "text", "text":f"Describe the image in detail. Based on your description, what lower case letter does the image look like? Based on this description:{description}, what letter does the image look like?"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encoded_string}"},
                }]
            },
        ],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    check_ghostscript()
    draw_q()
    letter = identify_letter_from_image()
    print(f"The letter is: {letter}")
    os.remove("q_letter.eps")  # Clean up the EPS file
    os.remove("q_letter.png")  # Clean up the PNG file
