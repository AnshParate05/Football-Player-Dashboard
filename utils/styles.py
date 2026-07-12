def load_css():
    return """
    <style>

    .main{
        background-color:#0E1117;
        color:white;
    }

    h1,h2,h3{
        color:white;
    }

    div[data-testid="metric-container"]{
        background:#1F2937;
        border-radius:12px;
        padding:18px;
        border:1px solid #374151;
        box-shadow:0px 4px 10px rgba(0,0,0,0.3);
    }

    section[data-testid="stSidebar"]{
        background:#111827;
    }

    </style>
    """