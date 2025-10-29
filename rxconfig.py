import reflex as rx

config = rx.Config(
    app_name="etr_checker",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)