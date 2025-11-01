def print_latin_square(latin_square):

    print("Latin Square:")
    for row in latin_square:
        print(" ".join(map(str, row)))

    return