
check = {
    'threads': 12,
}

exec(open(r'./server_app/fluent191_solver/prerequisite.py', 'r').read(), check)
print(check['runnable'])
