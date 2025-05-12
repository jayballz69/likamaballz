print("Simple test")
try:
    import ovos_workshop
    print(f"ovos_workshop modules: {dir(ovos_workshop)}")
    
    try:
        from ovos_workshop.skills.skill import MycroftSkill
        print("MycroftSkill found in ovos_workshop.skills.skill")
    except ImportError as e:
        print(f"Error importing MycroftSkill: {e}")
except ImportError as e:
    print(f"Error importing ovos_workshop: {e}")

try:
    import ovos_core
    print(f"ovos_core modules: {dir(ovos_core)}")
except ImportError as e:
    print(f"Error importing ovos_core: {e}")
