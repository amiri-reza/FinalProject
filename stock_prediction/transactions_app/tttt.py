def build_food(name, ingredients, is_vegan):
    def init(self, **kwargs):
        self.properties = kwargs

    return type(
        name,
        (object,),
        {"__init__": init, "ingredients": ingredients, "is_vegan": is_vegan},
    )


rice = build_food("rice", "rice", False)
print(dir(rice))


def add(num):
    hey = num + 2
    return hey


hi = add(5)
print(dir(hi))
