def load_stylesheet():
    return """
    QWidget {
        background-color: #1e1e1e;
        color : #f0f0f0;
        font-family : Segoe UI, sans-serif;
        font-size: 13px;
    }
    
    QTableWidget{
        background-color: #2e2e2e;
        gridline-color: #444;
        selection-background-color: #44475a;
    }
    
    QHeaderView::section {
        background-color: #3a3a3a;
        color: #ffffff;
        font-weight: bold;
        padding: 4px;
    }

    QPushButton {
        background-color: #44475a;
        color: white;
        border-radius: 4px;
        padding: 6px 10px;
    }

    QPushButton:hover {
        background-color: #6272a4;
    }

    QLabel {
        font-weight: bold;
    }
    
    
    """