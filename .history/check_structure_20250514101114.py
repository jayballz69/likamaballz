# See AI_CODING_BASELINE_RULES.md for required practices.

import os
import sys
import importlib

print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\nChecking for skills modules:")
packages = ['ovos_core', 'ovos_workshop']
for pkg in packages:
    try:
        mod = importlib.import_module(f"{pkg}.skills")
        print(f"{pkg}.skills: Successfully imported")
    except ImportError as e:
        print(f"{pkg}.skills: ImportError - {e}")
    
    try:
        mod = importlib.import_module(pkg)
        print(f"{pkg} modules: {dir(mod)}")
    except ImportError as e:
        print(f"{pkg}: ImportError - {e}")

print("\nMain OVOS modules:")
modules = ['ovos_core.__main__', 'ovos_core.main', 'ovos_skills_manager']
for mod_name in modules:
    try:
        mod = importlib.import_module(mod_name)
        print(f"{mod_name}: Successfully imported")
    except ImportError as e:
        print(f"{mod_name}: ImportError - {e}")

print("\nLooking for SkillService:")
possible_modules = [
    'ovos_core.skills.service',
    'ovos_workshop.skills.service',
    'ovos_workshop.service',
    'ovos_workshop.service.skill_service'
]

for mod_name in possible_modules:
    try:
        mod = importlib.import_module(mod_name)
        print(f"{mod_name}: Successfully imported")
        if hasattr(mod, 'SkillService'):
            print(f"  SkillService found in {mod_name}")
    except ImportError as e:
        print(f"{mod_name}: ImportError - {e}")
