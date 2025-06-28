#!/usr/bin/env python3
"""
Test file to debug Flet scrolling issues
Run this to verify scrolling works properly
"""

import flet as ft

def main(page: ft.Page):
    page.title = "Scrolling Test"
    page.window_width = 800
    page.window_height = 600
    page.scroll = None  # Disable page scroll
    
    # Create test content with many items
    test_items = []
    for i in range(4):
        section = ft.Container(
            content=ft.Column([
                ft.Text(f"Section {i+1}", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"This is section {i+1} content that should be visible"),
                ft.ElevatedButton(f"Button {i+1}", on_click=lambda e, x=i: print(f"Button {x+1} clicked")),
                ft.TextField(label=f"Input {i+1}"),
                ft.Container(
                    content=ft.Text("Some more content here\n" * 5),
                    bgcolor=ft.colors.BLUE_GREY_100,
                    padding=10,
                    border_radius=5
                )
            ]),
            bgcolor=ft.colors.GREY_200,
            padding=20,
            margin=10,
            border_radius=8
        )
        test_items.append(section)
        test_items.append(ft.Divider())
    
    # Method 1: Using ListView (RECOMMENDED)
    content_listview = ft.ListView(
        controls=test_items,
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=False
    )
    
    # Method 2: Using Column with scroll inside Container
    # content_column = ft.Column(
    #     controls=test_items,
    #     scroll=ft.ScrollMode.AUTO,
    #     spacing=10
    # )
    # 
    # content_container = ft.Container(
    #     content=content_column,
    #     expand=True,
    #     padding=20
    # )
    
    # Create tabs to test tab scrolling
    tabs = ft.Tabs(
        tabs=[
            ft.Tab(
                text="Test Tab 1",
                content=ft.Container(
                    content=content_listview,  # Use ListView method
                    expand=True
                )
            ),
            ft.Tab(
                text="Test Tab 2",
                content=ft.Container(
                    content=ft.Text("This is tab 2"),
                    expand=True
                )
            )
        ],
        expand=True
    )
    
    # Main layout
    page.add(
        ft.Column([
            ft.Container(
                content=ft.Text("Scrolling Test App", size=24, color="white"),
                bgcolor=ft.colors.BLUE,
                padding=20,
                height=60
            ),
            tabs
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    ft.app(target=main)