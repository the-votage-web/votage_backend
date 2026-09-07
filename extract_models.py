import os
import sys
import django

# Set up Django environment
sys.path.insert(0, '/root/programs/votage_pg/church')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'church.settings')
django.setup()

from django.apps import apps
from django.db import models

output_path = '/root/programs/votage_pg/church/DATA_MODELS.md'

with open(output_path, 'w', encoding='utf-8') as f:
    f.write('# Django Data Models Summary & Relationships\n\n')
    f.write('This document contains the complete data model schema and relationship diagrams for all applications in this project.\n\n')
    
    # -------------------------------------------------------------
    # 1. Mermaid ER Diagram
    # -------------------------------------------------------------
    f.write('## Entity Relationship Diagram (ERD)\n\n')
    f.write('```mermaid\nerDiagram\n')
    
    excluded_labels = {'admin', 'auth', 'contenttypes', 'sessions'}
    project_models = [m for m in apps.get_models() if m._meta.app_label not in excluded_labels]
    project_model_names = {m.__name__ for m in project_models}

    # Add entity declarations
    for model in project_models:
        f.write(f'    {model.__name__} {{\n')
        for field in model._meta.get_fields():
            if not field.is_relation and hasattr(field, 'get_internal_type'):
                ftype = field.get_internal_type()
                fname = field.name
                f.write(f'        {ftype} {fname}\n')
        f.write('    }\n')
    f.write('\n')

    # Add relationships
    seen_rels = set()
    for model in project_models:
        model_name = model.__name__
        for field in model._meta.get_fields():
            if field.is_relation and hasattr(field, 'related_model') and field.related_model:
                rel_model = field.related_model.__name__
                if rel_model in project_model_names:
                    rel_key = (model_name, field.name, rel_model)
                    if rel_key not in seen_rels:
                        seen_rels.add(rel_key)
                        if isinstance(field, models.ForeignKey):
                            f.write(f'    {rel_model} ||--o{{ {model_name} : "{field.name}"\n')
                        elif isinstance(field, models.OneToOneField):
                            f.write(f'    {rel_model} ||--|| {model_name} : "{field.name}"\n')
                        elif isinstance(field, models.ManyToManyField):
                            f.write(f'    {rel_model} }}|--|{{ {model_name} : "{field.name}"\n')
    f.write('```\n\n')
    
    # -------------------------------------------------------------
    # 2. Apps & Models Detailed Specification
    # -------------------------------------------------------------
    f.write('## Apps & Models Specification\n\n')
    
    app_configs = [a for a in apps.get_app_configs() if a.name.startswith('apps.')]
    
    for app in app_configs:
        app_models = [m for m in app.get_models() if m in project_models]
        if not app_models:
            continue
            
        f.write(f'### App: `{app.name}`\n\n')
        
        for model in app_models:
            f.write(f'#### Model: `{model.__name__}`\n')
            if model.__doc__:
                doc = model.__doc__.strip()
                if doc and not doc.startswith(model.__name__):
                    f.write(f'*{doc}*\n\n')
            
            f.write('| Field Name | Type | Related Model | Attributes / Constraints |\n')
            f.write('| --- | --- | --- | --- |\n')
            
            for field in model._meta.get_fields():
                field_name = field.name
                field_type = field.get_internal_type() if hasattr(field, 'get_internal_type') else type(field).__name__
                related = ''
                details = []
                
                if field.is_relation:
                    if field.related_model:
                        related = f'`{field.related_model.__name__}`'
                    if isinstance(field, models.ForeignKey):
                        details.append('ForeignKey')
                    elif isinstance(field, models.OneToOneField):
                        details.append('OneToOneField')
                    elif isinstance(field, models.ManyToManyField):
                        details.append('ManyToManyField')
                    elif getattr(field, 'one_to_many', False):
                        details.append('Reverse FK')
                    elif getattr(field, 'one_to_one', False):
                        details.append('Reverse OneToOne')
                
                if getattr(field, 'null', False):
                    details.append('null=True')
                if getattr(field, 'blank', False):
                    details.append('blank=True')
                if getattr(field, 'primary_key', False):
                    details.append('PK')
                if getattr(field, 'unique', False):
                    details.append('unique=True')
                if getattr(field, 'choices', None):
                    details.append('choices')
                    
                detail_str = ', '.join(details)
                f.write(f'| `{field_name}` | `{field_type}` | {related} | {detail_str} |\n')
            f.write('\n')

print(f'Successfully generated schema documentation at: {output_path}')
