from dynamic_prompt_importer import DynamicPromptImporter as DPI

dpi = DPI("vercel/next.js")  # or your own repo
print(dpi._list_children)
