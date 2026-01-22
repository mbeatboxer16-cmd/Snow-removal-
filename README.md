<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>除雪出来高管理 - SNOW OPS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Exo+2:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00d4ff;
            --primary-glow: rgba(0, 212, 255, 0.5);
            --secondary: #6366f1;
            --accent: #fbbf24;
            --bg: #0a0e27;
            --surface: #141b3d;
            --surface-light: #1e2749;
            --text: #e2e8f0;
            --text-dark: #94a3b8;
            --success: #10b981;
            --danger: #ef4444;
            --border: rgba(100, 116, 139, 0.3);
            --glow: 0 0 20px var(--primary-glow);
            --glow-strong: 0 0 30px var(--primary-glow), 0 0 60px var(--primary-glow);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Exo 2', -apple-system, BlinkMacSystemFont, 'Hiragino Sans', sans-serif;
            background: var(--bg);
            background-image: 
                radial-gradient(ellipse at top, rgba(0, 212, 255, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at bottom, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
            background-attachment: fixed;
            color: var(--text);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            padding-bottom: 90px;
            min-height: 100vh;
        }

        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 2px,
                    rgba(0, 212, 255, 0.03) 2px,
                    rgba(0, 212, 255, 0.03) 4px
                );
            pointer-events: none;
            z-index: 1;
        }

        .header {
            background: rgba(10, 14, 39, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 212, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
            color: white;
            padding: 1.5rem 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.75rem;
            font-weight: 900;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            background: linear-gradient(135deg, var(--primary) 0%, #fff 50%, var(--primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 40px var(--primary-glow);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .header-title::before {
            content: '❄️';
            font-size: 2rem;
            filter: drop-shadow(0 0 10px var(--primary));
            animation: rotate 8s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .header-subtitle {
            font-family: 'Exo 2', sans-serif;
            font-size: 0.875rem;
            opacity: 0.8;
            margin-top: 0.5rem;
            color: var(--primary);
            font-weight: 600;
            letter-spacing: 0.05em;
        }

        .nav-tabs {
            display: flex;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(10, 14, 39, 0.98);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(0, 212, 255, 0.3);
            z-index: 100;
            box-shadow: 0 -8px 32px rgba(0, 212, 255, 0.1);
            padding: 0.5rem;
            gap: 0.5rem;
        }

        .nav-tab {
            flex: 1;
            padding: 1rem 0.5rem;
            text-align: center;
            border: 2px solid var(--border);
            background: rgba(30, 39, 73, 0.4);
            color: var(--text-dark);
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
            border-radius: 16px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            position: relative;
            overflow: hidden;
        }

        .nav-tab::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            opacity: 0;
            transition: opacity 0.4s;
        }

        .nav-tab.active {
            color: var(--primary);
            background: rgba(0, 212, 255, 0.1);
            border-color: var(--primary);
            box-shadow: var(--glow), inset 0 0 20px rgba(0, 212, 255, 0.1);
            transform: translateY(-2px);
        }

        .nav-tab.active::before {
            opacity: 0.1;
        }

        .nav-tab:active {
            transform: translateY(0) scale(0.95);
        }

        .nav-icon {
            font-size: 1.75rem;
            filter: drop-shadow(0 0 8px currentColor);
            transition: all 0.3s;
        }

        .nav-tab.active .nav-icon {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        .container {
            padding: 1.5rem 1rem;
            max-width: 800px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .screen {
            display: none;
            animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .screen.active {
            display: block;
        }

        @keyframes fadeInUp {
            from { 
                opacity: 0; 
                transform: translateY(30px);
            }
            to { 
                opacity: 1; 
                transform: translateY(0);
            }
        }

        .card {
            background: rgba(20, 27, 61, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 24px;
            padding: 2rem 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
            transition: left 0.8s;
        }

        .card:hover::before {
            left: 100%;
        }

        .card-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            text-shadow: 0 0 20px var(--primary-glow);
        }

        .card-title::after {
            content: '';
            flex: 1;
            height: 2px;
            background: linear-gradient(to right, var(--primary), transparent);
            box-shadow: 0 0 10px var(--primary-glow);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--primary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .form-input {
            width: 100%;
            padding: 1rem 1.25rem;
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 16px;
            font-size: 1rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            background: rgba(30, 39, 73, 0.4);
            color: var(--text);
            font-family: 'Exo 2', sans-serif;
        }

        .form-input::placeholder {
            color: var(--text-dark);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary);
            background: rgba(30, 39, 73, 0.6);
            box-shadow: var(--glow), inset 0 0 20px rgba(0, 212, 255, 0.05);
            transform: translateY(-2px);
        }

        .btn {
            padding: 1.25rem 2rem;
            border: none;
            border-radius: 16px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            width: 100%;
            margin-top: 0.5rem;
            font-family: 'Exo 2', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            position: relative;
            overflow: hidden;
        }

        .btn::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s;
        }

        .btn:hover::before {
            transform: translateX(100%);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.3), 0 0 0 1px rgba(0, 212, 255, 0.5);
            border: 2px solid transparent;
        }

        .btn-primary:hover {
            box-shadow: var(--glow-strong), 0 0 0 1px rgba(0, 212, 255, 0.8);
            transform: translateY(-3px);
        }

        .btn-primary:active {
            transform: translateY(-1px) scale(0.98);
            box-shadow: 0 4px 16px rgba(0, 212, 255, 0.3);
        }

        .btn-secondary {
            background: rgba(30, 39, 73, 0.6);
            color: var(--primary);
            border: 2px solid var(--primary);
            box-shadow: inset 0 0 20px rgba(0, 212, 255, 0.1);
        }

        .btn-secondary:hover {
            background: rgba(0, 212, 255, 0.1);
            box-shadow: var(--glow);
        }

        .btn-success {
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
            color: white;
            box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
        }

        .btn-success:hover {
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.5);
            transform: translateY(-3px);
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%);
            color: white;
            box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);
        }

        .btn-danger:hover {
            box-shadow: 0 0 30px rgba(239, 68, 68, 0.5);
            transform: translateY(-3px);
        }

        .btn-small {
            padding: 0.625rem 1.25rem;
            font-size: 0.875rem;
            width: auto;
        }

        .btn-time {
            padding: 1rem;
            font-size: 0.875rem;
            border-radius: 12px;
            font-weight: 600;
            background: rgba(30, 39, 73, 0.6);
            border: 2px solid rgba(0, 212, 255, 0.3);
            color: var(--text);
        }

        .btn-time.active {
            background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
            border-color: var(--success);
            color: white;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.5);
        }

        .btn-time:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }

        .location-list {
            list-style: none;
        }

        .location-item {
            background: rgba(30, 39, 73, 0.4);
            backdrop-filter: blur(10px);
            padding: 1.25rem;
            border-radius: 16px;
            margin-bottom: 1rem;
            border: 2px solid rgba(0, 212, 255, 0.2);
            border-left: 4px solid var(--primary);
            display: flex;
            justify-content: space-between;
            align-items: start;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }

        .location-item:hover {
            border-color: var(--primary);
            box-shadow: var(--glow), 0 4px 16px rgba(0, 0, 0, 0.3);
            transform: translateX(5px);
        }

        .location-info {
            flex: 1;
        }

        .location-name {
            font-weight: 700;
            font-size: 1.125rem;
            color: var(--primary);
            margin-bottom: 0.5rem;
            text-shadow: 0 0 10px var(--primary-glow);
        }

        .location-address {
            font-size: 0.875rem;
            color: var(--text-dark);
            margin-bottom: 0.5rem;
        }

        .location-coords {
            font-size: 0.75rem;
            color: var(--text-dark);
            font-family: 'Courier New', monospace;
            background: rgba(0, 212, 255, 0.1);
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            display: inline-block;
        }

        .location-actions {
            display: flex;
            gap: 0.5rem;
        }

        .checkbox-item {
            background: rgba(30, 39, 73, 0.4);
            backdrop-filter: blur(10px);
            padding: 1.25rem;
            border-radius: 16px;
            margin-bottom: 1rem;
            border: 2px solid rgba(0, 212, 255, 0.2);
            display: flex;
            align-items: center;
            gap: 1rem;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .checkbox-item:hover {
            border-color: var(--primary);
            box-shadow: var(--glow);
        }

        .checkbox-item.selected {
            border-color: var(--primary);
            background: rgba(0, 212, 255, 0.1);
            box-shadow: var(--glow);
            transform: scale(1.02);
        }

        .checkbox-item input[type="checkbox"] {
            width: 28px;
            height: 28px;
            cursor: pointer;
            accent-color: var(--primary);
        }

        .work-item {
            background: rgba(30, 39, 73, 0.4);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 20px;
            margin-bottom: 1.5rem;
            border: 2px solid rgba(0, 212, 255, 0.2);
            border-left: 5px solid var(--secondary);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .work-item:hover {
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.3), 0 8px 24px rgba(0, 0, 0, 0.4);
            transform: translateY(-2px);
        }

        .work-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 1rem;
            gap: 1rem;
        }

        .work-order {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            min-width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 1.25rem;
            font-family: 'Orbitron', sans-serif;
            box-shadow: 0 0 20px var(--primary-glow);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }

        .work-name {
            flex: 1;
            padding: 0 1rem;
            font-weight: 700;
            font-size: 1.25rem;
            color: var(--text);
            line-height: 1.3;
        }

        .work-details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-top: 1rem;
        }

        .work-detail {
            background: rgba(20, 27, 61, 0.6);
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid rgba(0, 212, 255, 0.2);
            transition: all 0.3s;
        }

        .work-detail:hover {
            border-color: var(--primary);
            background: rgba(20, 27, 61, 0.8);
        }

        .work-detail-label {
            font-size: 0.75rem;
            color: var(--text-dark);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }

        .work-detail-value {
            font-size: 1.125rem;
            font-weight: 700;
            color: var(--primary);
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 10px var(--primary-glow);
        }

        .time-input-group {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }

        .time-input-group input {
            flex: 1;
        }

        .distance-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: linear-gradient(135deg, var(--accent) 0%, #f59e0b 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
            border: 2px solid rgba(255, 255, 255, 0.2);
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .summary-card {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(99, 102, 241, 0.2) 100%);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(0, 212, 255, 0.3);
            color: white;
            padding: 1.5rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0, 212, 255, 0.2);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .summary-card:hover {
            box-shadow: var(--glow-strong);
            transform: translateY(-5px) scale(1.03);
        }

        .summary-label {
            font-size: 0.75rem;
            opacity: 0.9;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }

        .summary-value {
            font-size: 2.5rem;
            font-weight: 900;
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 30px var(--primary-glow);
            line-height: 1;
        }

        .summary-unit {
            font-size: 1rem;
            opacity: 0.9;
            margin-left: 0.25rem;
            font-weight: 600;
        }

        .report-tabs {
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }

        .report-tab {
            flex: 1;
            padding: 1rem;
            border: 2px solid rgba(0, 212, 255, 0.3);
            background: rgba(30, 39, 73, 0.4);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            cursor: pointer;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            color: var(--text-dark);
        }

        .report-tab:hover {
            border-color: var(--primary);
        }

        .report-tab.active {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border-color: var(--primary);
            box-shadow: var(--glow);
        }

        .report-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(20, 27, 61, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(0, 212, 255, 0.2);
        }

        .report-table th {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 1.25rem;
            text-align: left;
            font-weight: 700;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .report-table td {
            padding: 1.25rem;
            border-bottom: 1px solid rgba(0, 212, 255, 0.1);
            font-size: 0.875rem;
            color: var(--text);
        }

        .report-table tr:last-child td {
            border-bottom: none;
        }

        .report-table tr:hover {
            background: rgba(0, 212, 255, 0.05);
        }

        .empty-state {
            text-align: center;
            padding: 4rem 1rem;
            color: var(--text-dark);
        }

        .empty-icon {
            font-size: 5rem;
            margin-bottom: 1.5rem;
            opacity: 0.3;
            filter: drop-shadow(0 0 20px var(--primary-glow));
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(10px);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            animation: fadeIn 0.3s;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: rgba(20, 27, 61, 0.95);
            backdrop-filter: blur(30px);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 24px;
            padding: 2rem 1.5rem;
            max-width: 500px;
            width: 100%;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), var(--glow);
            animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .modal-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.5rem;
            font-weight: 900;
            margin-bottom: 1.5rem;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            text-shadow: 0 0 20px var(--primary-glow);
            text-align: center;
        }

        .order-controls {
            display: flex;
            gap: 0.5rem;
        }

        .order-btn {
            background: rgba(30, 39, 73, 0.6);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 10px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-weight: 700;
            font-size: 1.125rem;
            color: var(--primary);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .order-btn:hover:not(:disabled) {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
            box-shadow: var(--glow);
            transform: scale(1.1);
        }

        .order-btn:disabled {
            opacity: 0.2;
            cursor: not-allowed;
        }

        @media print {
            .header, .nav-tabs, .btn {
                display: none;
            }
            .container {
                padding: 0;
            }
            .card {
                box-shadow: none;
                page-break-inside: avoid;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title">
            SNOW OPS
        </div>
        <div class="header-subtitle" id="currentDate"></div>
    </div>

    <div class="container">
        <!-- 契約先登録画面 -->
        <div id="screen-register" class="screen active">
            <div class="card">
                <div class="card-title">📍 新規契約先登録</div>
                <form id="locationForm">
                    <div class="form-group">
                        <label class="form-label">契約先名</label>
                        <input type="text" id="locationName" class="form-input" placeholder="例：○○商店" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">住所</label>
                        <input type="text" id="locationAddress" class="form-input" placeholder="例：○○市○○町1-2-3" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">緯度</label>
                        <input type="number" step="0.000001" id="locationLat" class="form-input" placeholder="例：35.681236" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">経度</label>
                        <input type="number" step="0.000001" id="locationLng" class="form-input" placeholder="例：139.767125" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">単価タイプ</label>
                        <select id="priceType" class="form-input" required>
                            <option value="flat">一式</option>
                            <option value="hourly">時間単価</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">単価（円）</label>
                        <input type="number" step="1" id="priceAmount" class="form-input" placeholder="例：10000" required>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        ✅ 登録する
                    </button>
                </form>
            </div>

            <div class="card">
                <div class="card-title">📋 登録済み契約先一覧</div>
                <ul id="locationList" class="location-list"></ul>
            </div>
        </div>

        <!-- 本日の除雪作業画面 -->
        <div id="screen-work" class="screen">
            <div class="card">
                <div class="card-title">🚜 本日の除雪作業</div>
                <button class="btn btn-primary" id="selectLocationsBtn">
                    除雪箇所を選択
                </button>
            </div>

            <div id="workListContainer"></div>

            <div class="card" id="workSummaryCard" style="display: none;">
                <div class="card-title">📊 本日の作業サマリー</div>
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-label">作業箇所</div>
                        <div class="summary-value" id="summaryLocations">0</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">総移動距離</div>
                        <div class="summary-value">
                            <span id="summaryDistance">0.0</span>
                            <span class="summary-unit">km</span>
                        </div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">作業時間</div>
                        <div class="summary-value">
                            <span id="summaryWorkTime">0</span>
                            <span class="summary-unit">分</span>
                        </div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-label">休憩時間</div>
                        <div class="summary-value">
                            <span id="summaryBreakTime">0</span>
                            <span class="summary-unit">分</span>
                        </div>
                    </div>
                </div>
                <div class="summary-grid" style="grid-template-columns: 1fr;">
                    <div class="summary-card" style="background: linear-gradient(135deg, rgba(251, 191, 36, 0.3) 0%, rgba(245, 158, 11, 0.3) 100%); border-color: rgba(251, 191, 36, 0.5);">
                        <div class="summary-label">💰 本日の総売上</div>
                        <div class="summary-value" style="color: var(--accent);">
                            <span style="font-size: 1.5rem;">¥</span>
                            <span id="summaryRevenue">0</span>
                        </div>
                    </div>
                </div>
                <button class="btn btn-success" id="saveWorkBtn">
                    💾 本日の作業を保存
                </button>
                <div id="saveStatus" style="margin-top: 1rem; text-align: center; color: var(--text-dark); font-size: 0.875rem;"></div>
            </div>
        </div>

        <!-- 出来高集計画面 -->
        <div id="screen-report" class="screen">
            <div class="card">
                <div class="card-title">📈 出来高集計</div>
                <div class="report-tabs">
                    <button class="report-tab active" data-period="daily">日次</button>
                    <button class="report-tab" data-period="weekly">週次</button>
                    <button class="report-tab" data-period="monthly">月次</button>
                </div>
                <div id="reportContent"></div>
                <button class="btn btn-secondary" id="exportReportBtn">
                    📄 印刷・PDF出力
                </button>
            </div>
        </div>
    </div>

    <!-- ナビゲーション -->
    <div class="nav-tabs">
        <button class="nav-tab active" data-screen="register">
            <div class="nav-icon">📍</div>
            <div>契約先</div>
        </button>
        <button class="nav-tab" data-screen="work">
            <div class="nav-icon">🚜</div>
            <div>作業</div>
        </button>
        <button class="nav-tab" data-screen="report">
            <div class="nav-icon">📈</div>
            <div>集計</div>
        </button>
    </div>

    <!-- 除雪箇所選択モーダル -->
    <div id="selectModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">除雪箇所を選択</div>
            <div id="selectLocationList"></div>
            <button class="btn btn-primary" id="confirmSelectionBtn">
                確定して順序設定へ
            </button>
        </div>
    </div>

    <!-- 順序設定モーダル -->
    <div id="orderModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">除雪順序を設定</div>
            <div id="orderLocationList"></div>
            <button class="btn btn-success" id="confirmOrderBtn">
                ✅ 確定
            </button>
        </div>
    </div>

    <script>
        // データストレージ
        const Storage = {
            get(key) {
                const data = localStorage.getItem(key);
                return data ? JSON.parse(data) : null;
            },
            set(key, value) {
                localStorage.setItem(key, JSON.stringify(value));
            },
            getArray(key) {
                return this.get(key) || [];
            }
        };

        // 距離計算（ヒュベニの公式）
        function calculateDistance(lat1, lng1, lat2, lng2) {
            const toRad = (deg) => deg * Math.PI / 180;
            const R = 6371; // 地球の半径（km）
            
            const dLat = toRad(lat2 - lat1);
            const dLng = toRad(lng2 - lng1);
            const lat1Rad = toRad(lat1);
            const lat2Rad = toRad(lat2);
            
            const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                     Math.cos(lat1Rad) * Math.cos(lat2Rad) *
                     Math.sin(dLng/2) * Math.sin(dLng/2);
            const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
            
            return R * c;
        }

        // 時間差計算（分）
        function calculateTimeDiff(start, end) {
            if (!start || !end) return 0;
            const [sh, sm] = start.split(':').map(Number);
            const [eh, em] = end.split(':').map(Number);
            const startMin = sh * 60 + sm;
            const endMin = eh * 60 + em;
            return endMin - startMin;
        }

        // 日付フォーマット
        function formatDate(date) {
            const d = new Date(date);
            return `${d.getFullYear()}/${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}`;
        }

        // 現在日時表示
        function updateCurrentDate() {
            const now = new Date();
            const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'short' };
            document.getElementById('currentDate').textContent = now.toLocaleDateString('ja-JP', options);
        }

        // 画面切り替え
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                const screenName = tab.dataset.screen;
                
                // タブの切り替え
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                // 画面の切り替え
                document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
                document.getElementById(`screen-${screenName}`).classList.add('active');
                
                // 集計画面の場合はレポート更新
                if (screenName === 'report') {
                    updateReport('daily');
                }
            });
        });

        // 契約先登録
        document.getElementById('locationForm').addEventListener('submit', (e) => {
            e.preventDefault();
            
            const location = {
                id: Date.now(),
                name: document.getElementById('locationName').value,
                address: document.getElementById('locationAddress').value,
                lat: parseFloat(document.getElementById('locationLat').value),
                lng: parseFloat(document.getElementById('locationLng').value),
                priceType: document.getElementById('priceType').value,
                priceAmount: parseFloat(document.getElementById('priceAmount').value)
            };
            
            const locations = Storage.getArray('locations');
            locations.push(location);
            Storage.set('locations', locations);
            
            e.target.reset();
            renderLocationList();
            alert('契約先を登録しました');
        });

        // 契約先一覧表示
        function renderLocationList() {
            const locations = Storage.getArray('locations');
            const list = document.getElementById('locationList');
            
            if (locations.length === 0) {
                list.innerHTML = '<div class="empty-state"><div class="empty-icon">📍</div>登録された契約先がありません</div>';
                return;
            }
            
            list.innerHTML = locations.map(loc => {
                // 既存データとの互換性のため、単価情報がない場合はデフォルト値を設定
                const priceType = loc.priceType || 'flat';
                const priceAmount = loc.priceAmount || 0;
                
                return `
                <li class="location-item">
                    <div class="location-info">
                        <div class="location-name">${loc.name}</div>
                        <div class="location-address">${loc.address}</div>
                        <div class="location-coords">📍 ${loc.lat.toFixed(6)}, ${loc.lng.toFixed(6)}</div>
                        <div style="margin-top: 0.5rem; display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(251, 191, 36, 0.2); padding: 0.25rem 0.75rem; border-radius: 8px; border: 1px solid rgba(251, 191, 36, 0.4);">
                            <span style="color: var(--accent); font-weight: 700;">💰 ${priceType === 'flat' ? '一式' : '時間'}</span>
                            <span style="color: var(--text); font-weight: 700; font-family: 'Orbitron', sans-serif;">${priceAmount.toLocaleString()}円${priceType === 'hourly' ? '/時間' : ''}</span>
                        </div>
                    </div>
                    <div class="location-actions">
                        <button class="btn btn-danger btn-small" onclick="deleteLocation(${loc.id})">削除</button>
                    </div>
                </li>
            `}).join('');
        }

        // 契約先削除
        window.deleteLocation = function(id) {
            if (!confirm('この契約先を削除しますか？')) return;
            
            let locations = Storage.getArray('locations');
            locations = locations.filter(loc => loc.id !== id);
            Storage.set('locations', locations);
            renderLocationList();
        };

        // 除雪箇所選択モーダル
        document.getElementById('selectLocationsBtn').addEventListener('click', () => {
            const locations = Storage.getArray('locations');
            const selectList = document.getElementById('selectLocationList');
            
            if (locations.length === 0) {
                alert('契約先を先に登録してください');
                return;
            }
            
            selectList.innerHTML = locations.map(loc => `
                <div class="checkbox-item" data-id="${loc.id}">
                    <input type="checkbox" id="loc-${loc.id}">
                    <label for="loc-${loc.id}" style="flex: 1; cursor: pointer;">
                        <div style="font-weight: 700;">${loc.name}</div>
                        <div style="font-size: 0.875rem; color: var(--text-light);">${loc.address}</div>
                    </label>
                </div>
            `).join('');
            
            // チェックボックスのイベント
            selectList.querySelectorAll('.checkbox-item').forEach(item => {
                const checkbox = item.querySelector('input[type="checkbox"]');
                item.addEventListener('click', (e) => {
                    if (e.target !== checkbox) {
                        checkbox.checked = !checkbox.checked;
                    }
                    item.classList.toggle('selected', checkbox.checked);
                });
            });
            
            document.getElementById('selectModal').classList.add('active');
        });

        // 選択確定
        document.getElementById('confirmSelectionBtn').addEventListener('click', () => {
            const selectedIds = Array.from(document.querySelectorAll('#selectLocationList input:checked'))
                .map(cb => parseInt(cb.id.replace('loc-', '')));
            
            if (selectedIds.length === 0) {
                alert('除雪箇所を選択してください');
                return;
            }
            
            document.getElementById('selectModal').classList.remove('active');
            showOrderModal(selectedIds);
        });

        // 順序設定モーダル
        function showOrderModal(locationIds) {
            const locations = Storage.getArray('locations');
            const selectedLocations = locationIds.map(id => locations.find(loc => loc.id === id));
            
            const orderList = document.getElementById('orderLocationList');
            orderList.innerHTML = selectedLocations.map((loc, index) => `
                <div class="work-item" data-id="${loc.id}">
                    <div class="work-header">
                        <div class="work-order">${index + 1}</div>
                        <div class="work-name">${loc.name}</div>
                        <div class="order-controls">
                            <button class="order-btn" onclick="moveUp(this)" ${index === 0 ? 'disabled' : ''}>▲</button>
                            <button class="order-btn" onclick="moveDown(this)" ${index === selectedLocations.length - 1 ? 'disabled' : ''}>▼</button>
                        </div>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('orderModal').classList.add('active');
        }

        // 順序変更
        window.moveUp = function(btn) {
            const item = btn.closest('.work-item');
            const prev = item.previousElementSibling;
            if (prev) {
                item.parentNode.insertBefore(item, prev);
                updateOrderNumbers();
            }
        };

        window.moveDown = function(btn) {
            const item = btn.closest('.work-item');
            const next = item.nextElementSibling;
            if (next) {
                item.parentNode.insertBefore(next, item);
                updateOrderNumbers();
            }
        };

        function updateOrderNumbers() {
            const items = document.querySelectorAll('#orderLocationList .work-item');
            items.forEach((item, index) => {
                item.querySelector('.work-order').textContent = index + 1;
                const upBtn = item.querySelector('.order-controls button:first-child');
                const downBtn = item.querySelector('.order-controls button:last-child');
                upBtn.disabled = index === 0;
                downBtn.disabled = index === items.length - 1;
            });
        }

        // 順序確定
        document.getElementById('confirmOrderBtn').addEventListener('click', () => {
            const orderedIds = Array.from(document.querySelectorAll('#orderLocationList .work-item'))
                .map(item => parseInt(item.dataset.id));
            
            document.getElementById('orderModal').classList.remove('active');
            createWorkList(orderedIds);
        });

        // 作業リスト作成
        function createWorkList(locationIds) {
            const locations = Storage.getArray('locations');
            const orderedLocations = locationIds.map(id => {
                const loc = locations.find(l => l.id === id);
                // 既存データとの互換性のため、単価情報がない場合はデフォルト値を設定
                if (!loc.priceType) {
                    loc.priceType = 'flat';
                    loc.priceAmount = 0;
                }
                return loc;
            });
            
            const container = document.getElementById('workListContainer');
            container.innerHTML = orderedLocations.map((loc, index) => {
                let distance = 0;
                if (index > 0) {
                    const prevLoc = orderedLocations[index - 1];
                    distance = calculateDistance(prevLoc.lat, prevLoc.lng, loc.lat, loc.lng);
                }
                
                return `
                    <div class="card">
                        <div class="work-item">
                            <div class="work-header">
                                <div class="work-order">${index + 1}</div>
                                <div class="work-name">${loc.name}</div>
                                ${index > 0 ? `<div class="distance-badge">🚗 ${distance.toFixed(1)} km</div>` : ''}
                            </div>
                            
                            <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(251, 191, 36, 0.15); border-radius: 12px; border: 2px solid rgba(251, 191, 36, 0.4); display: flex; align-items: center; gap: 1rem;">
                                <div style="flex: 1;">
                                    <div style="font-size: 0.75rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;">💰 単価</div>
                                    <div style="font-size: 1.125rem; font-weight: 700; color: var(--accent); font-family: 'Orbitron', sans-serif;">${loc.priceAmount.toLocaleString()}円${loc.priceType === 'hourly' ? '/時間' : ''}</div>
                                </div>
                                <div style="flex: 1;">
                                    <div style="font-size: 0.75rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600;">💵 予定金額</div>
                                    <div class="estimated-amount" data-index="${index}" style="font-size: 1.125rem; font-weight: 700; color: var(--accent); font-family: 'Orbitron', sans-serif;">-</div>
                                </div>
                            </div>

                            <div style="margin-top: 1rem;">
                                <div class="work-detail-label">🔧 作業時間</div>
                                <div style="display: flex; gap: 0.75rem; margin-bottom: 0.75rem;">
                                    <button class="btn btn-time work-start-btn" data-index="${index}" onclick="recordTime(this, 'work-start')" style="flex: 1;">
                                        ▶ 開始
                                    </button>
                                    <button class="btn btn-time work-end-btn" data-index="${index}" onclick="recordTime(this, 'work-end')" style="flex: 1;" disabled>
                                        ■ 終了
                                    </button>
                                </div>
                                <div class="work-detail-value" style="text-align: center; padding: 0.75rem; background: rgba(20, 27, 61, 0.6); border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.2);">
                                    <span class="work-time-display" data-index="${index}">--:-- ~ --:--</span>
                                </div>
                                <input type="hidden" class="work-start" data-index="${index}">
                                <input type="hidden" class="work-end" data-index="${index}">
                            </div>

                            <div style="margin-top: 1.5rem;">
                                <div class="work-detail-label">☕ 休憩時間</div>
                                <div style="display: flex; gap: 0.75rem; margin-bottom: 0.75rem;">
                                    <button class="btn btn-time break-start-btn" data-index="${index}" onclick="recordTime(this, 'break-start')" style="flex: 1;" disabled>
                                        ▶ 開始
                                    </button>
                                    <button class="btn btn-time break-end-btn" data-index="${index}" onclick="recordTime(this, 'break-end')" style="flex: 1;" disabled>
                                        ■ 終了
                                    </button>
                                </div>
                                <div class="work-detail-value" style="text-align: center; padding: 0.75rem; background: rgba(20, 27, 61, 0.6); border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.2);">
                                    <span class="break-time-display" data-index="${index}">--:-- ~ --:--</span>
                                </div>
                                <input type="hidden" class="break-start" data-index="${index}">
                                <input type="hidden" class="break-end" data-index="${index}">
                            </div>

                            <div style="margin-top: 1.5rem; padding: 1.25rem; background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(99, 102, 241, 0.1)); border-radius: 16px; border: 2px solid rgba(0, 212, 255, 0.3); text-align: center;">
                                <div class="work-detail-label">⏱️ 正味所要時間</div>
                                <div class="work-detail-value work-duration" data-index="${index}" style="font-size: 1.5rem; margin-top: 0.5rem;">-</div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            // 単価情報を保存（グローバル変数に）
            window.currentWorkLocations = orderedLocations;
            
            document.getElementById('workSummaryCard').style.display = 'block';
            calculateSummary();
        }

        // 時間記録
        window.recordTime = function(btn, type) {
            const index = btn.dataset.index;
            const now = new Date();
            const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
            
            if (type === 'work-start') {
                document.querySelector(`.work-start[data-index="${index}"]`).value = timeStr;
                document.querySelector(`.work-time-display[data-index="${index}"]`).textContent = timeStr + ' ~ --:--';
                btn.classList.add('active');
                btn.disabled = true;
                btn.innerHTML = '✓ 開始済';
                document.querySelector(`.work-end-btn[data-index="${index}"]`).disabled = false;
            } else if (type === 'work-end') {
                document.querySelector(`.work-end[data-index="${index}"]`).value = timeStr;
                const startTime = document.querySelector(`.work-start[data-index="${index}"]`).value;
                document.querySelector(`.work-time-display[data-index="${index}"]`).textContent = startTime + ' ~ ' + timeStr;
                btn.classList.add('active');
                btn.disabled = true;
                btn.innerHTML = '✓ 終了済';
                document.querySelector(`.break-start-btn[data-index="${index}"]`).disabled = false;
                calculateWorkDuration(index);
            } else if (type === 'break-start') {
                document.querySelector(`.break-start[data-index="${index}"]`).value = timeStr;
                document.querySelector(`.break-time-display[data-index="${index}"]`).textContent = timeStr + ' ~ --:--';
                btn.classList.add('active');
                btn.disabled = true;
                btn.innerHTML = '✓ 開始済';
                document.querySelector(`.break-end-btn[data-index="${index}"]`).disabled = false;
            } else if (type === 'break-end') {
                document.querySelector(`.break-end[data-index="${index}"]`).value = timeStr;
                const startTime = document.querySelector(`.break-start[data-index="${index}"]`).value;
                document.querySelector(`.break-time-display[data-index="${index}"]`).textContent = startTime + ' ~ ' + timeStr;
                btn.classList.add('active');
                btn.disabled = true;
                btn.innerHTML = '✓ 終了済';
                calculateWorkDuration(index);
            }
            
            calculateSummary();
        };

        // 作業時間計算
        function calculateWorkDuration(index) {
            const startInput = document.querySelector(`.work-start[data-index="${index}"]`);
            const endInput = document.querySelector(`.work-end[data-index="${index}"]`);
            const breakStartInput = document.querySelector(`.break-start[data-index="${index}"]`);
            const breakEndInput = document.querySelector(`.break-end[data-index="${index}"]`);
            const durationDiv = document.querySelector(`.work-duration[data-index="${index}"]`);
            const estimatedAmountDiv = document.querySelector(`.estimated-amount[data-index="${index}"]`);
            
            const workTime = calculateTimeDiff(startInput.value, endInput.value);
            const breakTime = calculateTimeDiff(breakStartInput.value, breakEndInput.value);
            const netTime = workTime - breakTime;
            
            if (workTime > 0) {
                durationDiv.textContent = `${netTime}分${breakTime > 0 ? ' (休憩' + breakTime + '分)' : ''}`;
                
                // 金額計算
                if (window.currentWorkLocations && window.currentWorkLocations[index]) {
                    const location = window.currentWorkLocations[index];
                    let amount = 0;
                    if (location.priceType === 'flat') {
                        amount = location.priceAmount || 0;
                    } else { // hourly
                        amount = Math.round((netTime / 60) * (location.priceAmount || 0));
                    }
                    if (estimatedAmountDiv) {
                        estimatedAmountDiv.textContent = `¥${amount.toLocaleString()}`;
                    }
                }
            } else {
                durationDiv.textContent = '-';
                if (estimatedAmountDiv) {
                    estimatedAmountDiv.textContent = '-';
                }
            }
            
            calculateSummary();
        }

        // サマリー計算
        function calculateSummary() {
            const locations = document.querySelectorAll('.work-item').length;
            let totalDistance = 0;
            let totalWorkTime = 0;
            let totalBreakTime = 0;
            let totalRevenue = 0;
            
            document.querySelectorAll('.distance-badge').forEach(badge => {
                const distance = parseFloat(badge.textContent.match(/[\d.]+/)[0]);
                totalDistance += distance;
            });
            
            document.querySelectorAll('.work-start').forEach((startInput, index) => {
                const endInput = document.querySelector(`.work-end[data-index="${index}"]`);
                const breakStartInput = document.querySelector(`.break-start[data-index="${index}"]`);
                const breakEndInput = document.querySelector(`.break-end[data-index="${index}"]`);
                
                const workTime = calculateTimeDiff(startInput.value, endInput.value);
                const breakTime = calculateTimeDiff(breakStartInput.value, breakEndInput.value);
                
                totalWorkTime += workTime;
                totalBreakTime += breakTime;
                
                // 金額計算
                if (workTime > 0 && window.currentWorkLocations && window.currentWorkLocations[index]) {
                    const location = window.currentWorkLocations[index];
                    const netTime = workTime - breakTime;
                    if (location.priceType === 'flat') {
                        totalRevenue += location.priceAmount || 0;
                    } else { // hourly
                        totalRevenue += Math.round((netTime / 60) * (location.priceAmount || 0));
                    }
                }
            });
            
            document.getElementById('summaryLocations').textContent = locations;
            document.getElementById('summaryDistance').textContent = totalDistance.toFixed(1);
            document.getElementById('summaryWorkTime').textContent = totalWorkTime - totalBreakTime;
            document.getElementById('summaryBreakTime').textContent = totalBreakTime;
            document.getElementById('summaryRevenue').textContent = totalRevenue.toLocaleString();
        }

        // 作業保存
        document.getElementById('saveWorkBtn').addEventListener('click', () => {
            const statusDiv = document.getElementById('saveStatus');
            
            try {
                statusDiv.textContent = '保存中...';
                statusDiv.style.color = 'var(--primary)';
                console.log('保存開始');
                
                // 作業データがあるか確認
                if (!window.currentWorkLocations || window.currentWorkLocations.length === 0) {
                    statusDiv.textContent = 'エラー: 保存する作業データがありません';
                    statusDiv.style.color = 'var(--danger)';
                    alert('保存する作業データがありません');
                    return;
                }
                
                const workData = {
                    date: new Date().toISOString().split('T')[0],
                    timestamp: Date.now(),
                    locations: []
                };
                
                document.querySelectorAll('.work-item').forEach((item, index) => {
                    try {
                        const location = window.currentWorkLocations[index];
                        if (!location) {
                            console.warn(`Location ${index} not found`);
                            return;
                        }
                        
                        const startInput = document.querySelector(`.work-start[data-index="${index}"]`);
                        const endInput = document.querySelector(`.work-end[data-index="${index}"]`);
                        const breakStartInput = document.querySelector(`.break-start[data-index="${index}"]`);
                        const breakEndInput = document.querySelector(`.break-end[data-index="${index}"]`);
                        
                        const workTime = calculateTimeDiff(startInput.value, endInput.value);
                        const breakTime = calculateTimeDiff(breakStartInput.value, breakEndInput.value);
                        const netTime = workTime - breakTime;
                        
                        // 金額計算
                        let amount = 0;
                        const priceType = location.priceType || 'flat';
                        const priceAmount = location.priceAmount || 0;
                        
                        if (priceType === 'flat') {
                            amount = priceAmount;
                        } else { // hourly
                            amount = Math.round((netTime / 60) * priceAmount);
                        }
                        
                        workData.locations.push({
                            locationId: location.id,
                            name: location.name,
                            workStart: startInput.value || '',
                            workEnd: endInput.value || '',
                            breakStart: breakStartInput.value || '',
                            breakEnd: breakEndInput.value || '',
                            priceType: priceType,
                            priceAmount: priceAmount,
                            calculatedAmount: amount,
                            netWorkTime: netTime
                        });
                    } catch (itemError) {
                        console.error(`Error processing item ${index}:`, itemError);
                    }
                });
                
                console.log('保存データ:', workData);
                
                if (workData.locations.length === 0) {
                    statusDiv.textContent = 'エラー: 保存する作業データがありません';
                    statusDiv.style.color = 'var(--danger)';
                    alert('保存する作業データがありません');
                    return;
                }
                
                const workRecords = Storage.getArray('workRecords');
                workRecords.push(workData);
                Storage.set('workRecords', workRecords);
                
                console.log('保存完了');
                statusDiv.textContent = '✅ 保存成功！';
                statusDiv.style.color = 'var(--success)';
                alert('本日の作業を保存しました！');
                
                // 作業リストをクリア
                setTimeout(() => {
                    document.getElementById('workListContainer').innerHTML = '';
                    document.getElementById('workSummaryCard').style.display = 'none';
                    window.currentWorkLocations = null;
                }, 1000);
                
            } catch (error) {
                console.error('保存エラー:', error);
                statusDiv.textContent = '❌ 保存失敗: ' + error.message;
                statusDiv.style.color = 'var(--danger)';
                alert('保存に失敗しました: ' + error.message);
            }
        });

        // レポート表示
        function updateReport(period) {
            const workRecords = Storage.getArray('workRecords');
            const locations = Storage.getArray('locations');
            const reportContent = document.getElementById('reportContent');
            
            if (workRecords.length === 0) {
                reportContent.innerHTML = '<div class="empty-state"><div class="empty-icon">📊</div>作業記録がありません</div>';
                return;
            }
            
            let filteredRecords = workRecords;
            const now = new Date();
            
            if (period === 'weekly') {
                const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                filteredRecords = workRecords.filter(r => new Date(r.date) >= weekAgo);
            } else if (period === 'monthly') {
                const monthAgo = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate());
                filteredRecords = workRecords.filter(r => new Date(r.date) >= monthAgo);
            }
            
            // 契約先ごとの集計
            const summary = {};
            filteredRecords.forEach(record => {
                record.locations.forEach(loc => {
                    if (!summary[loc.locationId]) {
                        // 契約先情報を取得
                        const locationInfo = locations.find(l => l.id === loc.locationId) || {};
                        
                        summary[loc.locationId] = {
                            name: loc.name,
                            count: 0,
                            totalTime: 0,
                            totalRevenue: 0,
                            priceType: loc.priceType || locationInfo.priceType || 'flat',
                            priceAmount: loc.priceAmount || locationInfo.priceAmount || 0,
                            workDetails: []
                        };
                    }
                    summary[loc.locationId].count++;
                    
                    // 旧データとの互換性
                    if (loc.netWorkTime !== undefined) {
                        summary[loc.locationId].totalTime += loc.netWorkTime;
                    } else {
                        const workTime = calculateTimeDiff(loc.workStart, loc.workEnd);
                        const breakTime = calculateTimeDiff(loc.breakStart, loc.breakEnd);
                        summary[loc.locationId].totalTime += (workTime - breakTime);
                    }
                    
                    // 金額集計
                    if (loc.calculatedAmount !== undefined) {
                        summary[loc.locationId].totalRevenue += loc.calculatedAmount;
                    }
                    
                    // 作業詳細を保存
                    summary[loc.locationId].workDetails.push({
                        date: record.date,
                        workStart: loc.workStart,
                        workEnd: loc.workEnd,
                        breakStart: loc.breakStart,
                        breakEnd: loc.breakEnd,
                        netWorkTime: loc.netWorkTime,
                        calculatedAmount: loc.calculatedAmount || 0
                    });
                });
            });
            
            const summaryArray = Object.values(summary).map(s => ({
                ...s,
                avgTime: s.totalTime / s.count
            }));
            
            // 総売上計算
            const totalRevenue = summaryArray.reduce((sum, s) => sum + s.totalRevenue, 0);
            const totalWorkTime = summaryArray.reduce((sum, s) => sum + s.totalTime, 0);
            
            reportContent.innerHTML = `
                <div style="margin-bottom: 1.5rem;">
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
                        <div style="padding: 1.25rem; background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(245, 158, 11, 0.2)); border-radius: 16px; border: 2px solid rgba(251, 191, 36, 0.4); text-align: center;">
                            <div style="font-size: 0.75rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.5rem;">💰 期間総売上</div>
                            <div style="font-size: 2rem; font-weight: 900; color: var(--accent); font-family: 'Orbitron', sans-serif; text-shadow: 0 0 30px rgba(251, 191, 36, 0.5);">
                                ¥${totalRevenue.toLocaleString()}
                            </div>
                        </div>
                        <div style="padding: 1.25rem; background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(99, 102, 241, 0.2)); border-radius: 16px; border: 2px solid rgba(0, 212, 255, 0.3); text-align: center;">
                            <div style="font-size: 0.75rem; color: var(--primary); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.5rem;">⏱️ 総作業時間</div>
                            <div style="font-size: 2rem; font-weight: 900; color: var(--primary); font-family: 'Orbitron', sans-serif; text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);">
                                ${totalWorkTime}<span style="font-size: 1rem; opacity: 0.9; margin-left: 0.25rem;">分</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="overflow-x: auto;">
                    <table class="report-table">
                        <thead>
                            <tr>
                                <th>契約先</th>
                                <th>単価</th>
                                <th>作業回数</th>
                                <th>総作業時間</th>
                                <th>平均所要時間</th>
                                <th>売上金額</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${summaryArray.map(s => `
                                <tr style="cursor: pointer;" onclick="toggleDetails('details-${s.name.replace(/[^a-zA-Z0-9]/g, '')}')">
                                    <td>
                                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                                            <span style="font-size: 0.75rem;">▶</span>
                                            <strong>${s.name}</strong>
                                        </div>
                                    </td>
                                    <td>
                                        <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                                            <span style="color: var(--accent); font-weight: 600;">${s.priceType === 'flat' ? '一式' : '時間'}</span>
                                            <span style="font-family: 'Orbitron', sans-serif; font-weight: 700;">¥${s.priceAmount.toLocaleString()}</span>
                                        </div>
                                    </td>
                                    <td>${s.count}回</td>
                                    <td>${s.totalTime}分</td>
                                    <td>${Math.round(s.avgTime)}分</td>
                                    <td style="font-weight: 700; color: var(--accent); font-family: 'Orbitron', sans-serif;">¥${s.totalRevenue.toLocaleString()}</td>
                                </tr>
                                <tr id="details-${s.name.replace(/[^a-zA-Z0-9]/g, '')}" style="display: none;">
                                    <td colspan="6" style="background: rgba(0, 212, 255, 0.05); padding: 1.5rem;">
                                        <div style="font-weight: 700; margin-bottom: 1rem; color: var(--primary);">📋 作業履歴</div>
                                        <div style="display: grid; gap: 0.75rem;">
                                            ${s.workDetails.map(detail => `
                                                <div style="background: rgba(20, 27, 61, 0.6); padding: 1rem; border-radius: 12px; border: 1px solid rgba(0, 212, 255, 0.2);">
                                                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                                                        <div>
                                                            <div style="font-size: 0.75rem; color: var(--text-dark); margin-bottom: 0.25rem;">日付</div>
                                                            <div style="font-weight: 600;">${formatDate(detail.date)}</div>
                                                        </div>
                                                        <div>
                                                            <div style="font-size: 0.75rem; color: var(--text-dark); margin-bottom: 0.25rem;">作業時間</div>
                                                            <div style="font-weight: 600;">${detail.workStart || '--:--'} ~ ${detail.workEnd || '--:--'}</div>
                                                        </div>
                                                        <div>
                                                            <div style="font-size: 0.75rem; color: var(--text-dark); margin-bottom: 0.25rem;">休憩時間</div>
                                                            <div style="font-weight: 600;">${detail.breakStart || '--:--'} ~ ${detail.breakEnd || '--:--'}</div>
                                                        </div>
                                                        <div>
                                                            <div style="font-size: 0.75rem; color: var(--text-dark); margin-bottom: 0.25rem;">正味時間</div>
                                                            <div style="font-weight: 600; color: var(--primary);">${detail.netWorkTime || 0}分</div>
                                                        </div>
                                                        <div>
                                                            <div style="font-size: 0.75rem; color: var(--text-dark); margin-bottom: 0.25rem;">売上</div>
                                                            <div style="font-weight: 700; color: var(--accent); font-family: 'Orbitron', sans-serif;">¥${detail.calculatedAmount.toLocaleString()}</div>
                                                        </div>
                                                    </div>
                                                </div>
                                            `).join('')}
                                        </div>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }
        
        // 詳細表示切り替え
        window.toggleDetails = function(id) {
            const detailRow = document.getElementById(id);
            const isVisible = detailRow.style.display !== 'none';
            detailRow.style.display = isVisible ? 'none' : 'table-row';
            
            // 矢印の向きを変更
            const parentRow = detailRow.previousElementSibling;
            const arrow = parentRow.querySelector('span');
            if (arrow) {
                arrow.textContent = isVisible ? '▶' : '▼';
            }
        };

        // レポート期間タブ
        document.querySelectorAll('.report-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.report-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                updateReport(tab.dataset.period);
            });
        });

        // PDF出力
        document.getElementById('exportReportBtn').addEventListener('click', () => {
            window.print();
        });

        // 初期化
        updateCurrentDate();
        renderLocationList();
        setInterval(updateCurrentDate, 60000);
        
        // イベントリスナーが正しく登録されたか確認
        console.log('アプリ初期化完了');
        console.log('saveWorkBtn:', document.getElementById('saveWorkBtn'));
    </script>
</body>
</html>
