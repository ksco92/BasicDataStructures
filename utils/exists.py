def exists(value, structure):
    aux = structure.head

    while aux:
        if aux.value == value:
            return True
        aux = aux.next_node

    return False
