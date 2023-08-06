def show_scimmia(name):
    
    if name == "simo":
        print("This species of monkey is very stupid!")
        response = requests.get('https://media-exp1.licdn.com/dms/image/C4D03AQHDzxlACe4jpw/profile-displayphoto-shrink_200_200/0/1605116657172?e=1613606400&v=beta&t=EutF9Onxca5halTZA37F7IH2wQame9RrP8NH1KHzmqk')
        img = Image.open(BytesIO(response.content))
        img

    if name == "tia":
        print("This species of monkey is very clever!")
        response = requests.get('https://media-exp1.licdn.com/dms/image/C5603AQEFmnqoYx516w/profile-displayphoto-shrink_200_200/0/1570549530641?e=1613606400&v=beta&t=EwEb_42U7WOON8M12hIdEAUHwOilhO92kzF-K5uOYg8')
        img = Image.open(BytesIO(response.content))
        img

    else:
        print("This species of monkey is not known!")
        pass

    return img

