print("Simple test")\ntry:\n    import ovos_workshop\n    print(f"ovos_workshop modules: {dir(ovos_workshop)}")\nexcept ImportError as e:\n    print(f"Error importing ovos_workshop: {e}")
