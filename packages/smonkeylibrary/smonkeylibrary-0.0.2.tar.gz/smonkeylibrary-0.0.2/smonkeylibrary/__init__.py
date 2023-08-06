def show_scimmia(name):
    
    if name == "simo":
        print("This species of monkey is very stupid!")
        image = Image.open('simone.jpg')
        image.show()

    if name == "tia":
        print("This species of monkey is very clever!")
        image = Image.open('mattia.jpg')    
        image.show()

    else:
        print("This species of monkey is not known!")

    return image

