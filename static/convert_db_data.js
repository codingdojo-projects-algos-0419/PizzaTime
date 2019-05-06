var size_table={
    {% for size in sizes %}
    {{size.id}}:{
        'name': '{{size.name}},
        'description': '{{size.description}}',
        {% if not size.scaling: %}
        'scaling': 1,
        {% else %}
        'scaling': {{size.scaling}}',
        {% endif %}
        'price' : {{size.price}}
    },
    {% endfor %}
    placeholder:0
}

var style_table={
    {% for style in styles %}
    {{style.id}}:{
        'name': '{{style.name}}',
        'description': '{{style.description}}',
        'price' : {{style.price}}
    },
    {% endfor %}
    placeholder:0
};

var topping_menu_table={
    {% for topping in topping_menu %}
    {{topping.id}}:{
        'name': '{{topping.name}}'
        'description': '{{topping.description}}',
        'price' : {{topping.price}}
    },
    {% endfor %}
    placeholder:0
};