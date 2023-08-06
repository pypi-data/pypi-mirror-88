from typing import Dict, List, Union


class tag():
    def __init__(
        self,
        name: str,
        attrs: Dict[str, str] = {}
    ):
        self.name = name
        self.attrs = attrs
        self.children: List[Union[str, tag]] = []

    def append(self, child):
        self.children.append(child)

    def __getitem__(self, key):
        if type(key) is tuple:
            for c in key:
                self.append(c)
        else:
            self.append(key)

        return self

    def __str__(self):
        content = ''.join([str(c) for c in self.children])
        if not self.attrs:
            return f'<{self.name}>{content}</{self.name}>'

        attrs = ' '.join([f"{key}='{val}'" for key, val in self.attrs.items()])
        return f'<{self.name} {attrs}>{content}</{self.name}>'

    def __call__(self, attrs: Dict[str, str] = {}, **kwargs):
        self.attrs = {
            **self.attrs,
            **attrs,
            **kwargs
        }
        return self


class tag_maker():
    def __init__(self, name):
        self.name = name

    def __call__(self, attrs: Dict[str, str] = {}, **kwargs):
        return tag(self.name, {**attrs, **kwargs})

    def __getitem__(self, key):
        if type(key) is tag_maker:
            key = key()

        return tag(self.name)[key]

    def __getattr__(self, key):
        return self({'class': key})

    def __str__(self):
        return f'<{self.name}></{self.name}>'
