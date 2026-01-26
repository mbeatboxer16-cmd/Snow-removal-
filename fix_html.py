#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SNOW OPS 除雪管理アプリ 自動修正スクリプト
使い方: python3 fix_html.py 元のファイル.html
出力: 元のファイル_fixed.html
"""

import sys
import re

def fix_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("修正を開始します...")
    
    # ①修正：getTodayDateString関数を追加
    print("①日付変更時間を0:00に修正中...")
    
    # calculateTimeDiff関数の後に追加
    if 'function getTodayDateString()' not in content:
        date_func = '''
        // ①修正：本日の日付を取得（0:00基準）
        function getTodayDateString() {
            const now = new Date();
            return now.toISOString().split('T')[0];
        }'''
        
        content = content.replace(
            'function calculateTimeDiff(start, end) {',
            date_func + '\n\n        function calculateTimeDiff(start, end) {'
        )
    
    # 作業保存処理を修正
    content = re.sub(
        r"date: new Date\(\)\.toISOString\(\)\.split\('T'\)\[0\],",
        "date: getTodayDateString(), // ①修正：0:00基準の日付を使用",
        content
    )
    
    # ②修正：契約先別集計の単価表示
    print("②契約先別集計の単価表示を修正中...")
    
    # summary作成部分を修正
    old_summary = r"priceType: loc\.priceType \|\| 'flat',\s*priceAmount: loc\.priceAmount \|\| 0,"
    new_summary = """priceType: loc.priceType || locationInfo.priceType || 'flat',
                            dayPrice: loc.dayPrice || locationInfo.dayPrice || 0,
                            nightPrice: loc.nightPrice || locationInfo.nightPrice || 0,"""
    content = re.sub(old_summary, new_summary, content)
    
    # 単価表示HTMLを修正
    old_price_display = r"<span style=\"color: var\(--accent\); font-weight: 600;\">\$\{s\.priceType === 'flat' \? '一式' : '時間'\}</span>\s*<span style=\"font-family: 'Orbitron', sans-serif; font-weight: 700;\">\$\{s\.priceAmount\.toLocaleString\(\)\}円</span>"
    
    new_price_display = """<span style="color: var(--accent); font-weight: 600;">${s.priceType === 'flat' ? '一式' : '時間'}</span>
                                            <div style="font-family: 'Orbitron', sans-serif; font-weight: 700; font-size: 0.75rem;">
                                                <div style="color: var(--accent);">🌞¥${s.dayPrice.toLocaleString()}</div>
                                                <div style="color: var(--primary);">🌙¥${s.nightPrice.toLocaleString()}</div>
                                            </div>"""
    
    content = re.sub(old_price_display, new_price_display, content, flags=re.DOTALL)
    
    # ③修正：作業履歴プルダウン全件対応
    print("③作業履歴プルダウンを修正中...")
    
    # テーブル行のマップを修正（名前ベースからindexベースへ）
    content = re.sub(
        r"\$\{summaryArray\.map\(s => `",
        "${summaryArray.map((s, index) => `",
        content
    )
    
    content = re.sub(
        r"onclick=\"toggleDetails\('details-\$\{s\.name\.replace\(/\[^a-zA-Z0-9\]/g, ''\)\}'\)\"",
        "onclick=\"toggleDetails('details-${index}')\"",
        content
    )
    
    content = re.sub(
        r"<span style=\"font-size: 0\.75rem;\">▶</span>",
        '<span class="toggle-arrow" id="arrow-${index}" style="font-size: 0.75rem;">▶</span>',
        content
    )
    
    content = re.sub(
        r"<tr id=\"details-\$\{s\.name\.replace\(/\[^a-zA-Z0-9\]/g, ''\)\}\" style=\"display: none;\">",
        '<tr id="details-${index}" style="display: none;">',
        content
    )
    
    # toggleDetails関数を修正
    old_toggle = r"window\.toggleDetails = function\(id\) \{[^}]+const parentRow = detailRow\.previousElementSibling;[^}]+\};"
    
    new_toggle = """window.toggleDetails = function(id) {
            const detailRow = document.getElementById(id);
            const arrowId = id.replace('details-', 'arrow-');
            const arrow = document.getElementById(arrowId);
            
            const isVisible = detailRow.style.display !== 'none';
            detailRow.style.display = isVisible ? 'none' : 'table-row';
            
            if (arrow) {
                arrow.textContent = isVisible ? '▶' : '▼';
            }
        };"""
    
    content = re.sub(old_toggle, new_toggle, content, flags=re.DOTALL)
    
    # ④修正：日別作業記録に稼働時間表示
    print("④日別作業記録に稼働時間を追加中...")
    
    # 稼働時間計算コードを追加
    working_hours_calc = """
                            // ④修正：稼働時間を計算（最も早い開始時刻 ～ 最も遅い終了時刻）
                            let earliestStart = null;
                            let latestEnd = null;
                            record.locations.forEach(loc => {
                                if (loc.workStart && (!earliestStart || loc.workStart < earliestStart)) {
                                    earliestStart = loc.workStart;
                                }
                                if (loc.workEnd && (!latestEnd || loc.workEnd > latestEnd)) {
                                    latestEnd = loc.workEnd;
                                }
                            });
                            const workingHours = earliestStart && latestEnd ? `${earliestStart} ～ ${latestEnd}` : '時刻不明';
                            """
    
    # recordTime計算の直後に挿入
    content = re.sub(
        r"(const recordTime = record\.locations\.reduce\(\(sum, loc\) => sum \+ \(loc\.netWorkTime \|\| 0\), 0\);)",
        r"\1" + working_hours_calc,
        content
    )
    
    # 稼働時間表示を追加
    working_hours_display = """<div>
                                            <span style="color: var(--text-dark);">稼働時間:</span>
                                            <span style="color: var(--primary); font-weight: 700; margin-left: 0.25rem;">${workingHours}</span>
                                        </div>
                                        """
    
    content = re.sub(
        r"(<div>\s*<span style=\"color: var\(--text-dark\);\">作業時間:</span>)",
        working_hours_display + r"\1",
        content
    )
    
    # ⑤修正：日別作業記録PDF出力ボタンとイベントを追加
    print("⑤日別作業PDF出力機能を追加中...")
    
    # PDFボタンのテキスト修正
    content = content.replace(
        '📄 PDF出力',
        '📄 契約先別PDF'
    )
    
    # 日別PDFボタンを追加
    daily_pdf_button = """
                <div style="margin-top: 0.75rem;">
                    <button class="btn btn-primary" id="exportDailyReportBtn">
                        📄 日別作業PDF
                    </button>
                </div>"""
    
    content = re.sub(
        r"(</div>\s*</div>\s*</div>\s*<!-- ナビゲーション -->)",
        daily_pdf_button + r"\n        \1",
        content
    )
    
    # 日別PDF生成関数を追加（既存のgenerateReportPDF関数の後）
    daily_pdf_code = """
        
        // ⑤修正：日別作業記録PDF出力機能追加
        document.getElementById('exportDailyReportBtn').addEventListener('click', () => {
            try {
                const activeTab = document.querySelector('.report-tab.active');
                const period = activeTab ? activeTab.dataset.period : 'daily';
                
                const workRecords = Storage.getArray('workRecords');
                
                if (workRecords.length === 0) {
                    alert('エクスポートする作業記録がありません');
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
                
                generateDailyReportPDF(period, filteredRecords);
                
            } catch (error) {
                console.error('Daily report export error:', error);
                alert('❌ 日別レポートのエクスポートに失敗しました: ' + error.message);
            }
        });
        
        // 日別作業記録PDF生成関数
        function generateDailyReportPDF(period, records) {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF({
                orientation: 'landscape',
                unit: 'mm',
                format: 'a4'
            });
            
            const periodName = period === 'daily' ? '日次' : period === 'weekly' ? '週次' : '月次';
            const dateStr = new Date().toLocaleDateString('ja-JP', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
            });
            
            doc.setFontSize(18);
            doc.text('除雪作業 日別記録一覧', 148, 15, { align: 'center' });
            
            doc.setFontSize(12);
            doc.text(`${periodName}レポート`, 148, 23, { align: 'center' });
            doc.text(`出力日: ${dateStr}`, 148, 30, { align: 'center' });
            
            const headers = [
                ['日付', '作業箇所', '稼働時間', '作業時間\\n(分)', '売上金額\\n(円)']
            ];
            
            const sortedRecords = records.sort((a, b) => new Date(b.date) - new Date(a.date));
            
            const data = sortedRecords.map(record => {
                const recordRevenue = record.locations.reduce((sum, loc) => sum + (loc.calculatedAmount || 0), 0);
                const recordTime = record.locations.reduce((sum, loc) => sum + (loc.netWorkTime || 0), 0);
                
                let earliestStart = null;
                let latestEnd = null;
                record.locations.forEach(loc => {
                    if (loc.workStart && (!earliestStart || loc.workStart < earliestStart)) {
                        earliestStart = loc.workStart;
                    }
                    if (loc.workEnd && (!latestEnd || loc.workEnd > latestEnd)) {
                        latestEnd = loc.workEnd;
                    }
                });
                const workingHours = earliestStart && latestEnd ? `${earliestStart}～${latestEnd}` : '-';
                
                return [
                    formatDate(record.date),
                    record.locations.length + '箇所',
                    workingHours,
                    recordTime,
                    '¥' + recordRevenue.toLocaleString()
                ];
            });
            
            const totalLocations = sortedRecords.reduce((sum, r) => sum + r.locations.length, 0);
            const totalTime = sortedRecords.reduce((sum, r) => {
                return sum + r.locations.reduce((s, loc) => s + (loc.netWorkTime || 0), 0);
            }, 0);
            const totalRevenue = sortedRecords.reduce((sum, r) => {
                return sum + r.locations.reduce((s, loc) => s + (loc.calculatedAmount || 0), 0);
            }, 0);
            
            data.push([
                '合計',
                totalLocations + '箇所',
                '-',
                totalTime,
                '¥' + totalRevenue.toLocaleString()
            ]);
            
            doc.autoTable({
                startY: 40,
                head: headers,
                body: data,
                theme: 'grid',
                styles: {
                    font: 'helvetica',
                    fontSize: 10,
                    cellPadding: 3,
                    overflow: 'linebreak',
                    halign: 'center',
                    valign: 'middle'
                },
                headStyles: {
                    fillColor: [0, 212, 255],
                    textColor: [255, 255, 255],
                    fontStyle: 'bold',
                    fontSize: 11
                },
                columnStyles: {
                    0: { halign: 'center', cellWidth: 35 },
                    1: { halign: 'center', cellWidth: 30 },
                    2: { halign: 'center', cellWidth: 40 },
                    3: { halign: 'right', cellWidth: 30 },
                    4: { halign: 'right', cellWidth: 50 }
                },
                didParseCell: function(data) {
                    if (data.row.index === sortedRecords.length) {
                        data.cell.styles.fontStyle = 'bold';
                        data.cell.styles.fillColor = [240, 240, 240];
                    }
                }
            });
            
            const pageCount = doc.internal.getNumberOfPages();
            for (let i = 1; i <= pageCount; i++) {
                doc.setPage(i);
                doc.setFontSize(9);
                doc.text(
                    `SNOW OPS - 除雪出来高管理システム   ページ ${i} / ${pageCount}`,
                    148,
                    200,
                    { align: 'center' }
                );
            }
            
            doc.save(`除雪日別記録_${periodName}_${dateStr.replace(/\\//g, '')}.pdf`);
            
            alert(`✅ 日別作業記録をPDF出力しました！\\n\\n作業日数: ${sortedRecords.length}日\\n総売上: ¥${totalRevenue.toLocaleString()}`);
        }"""
    
    # レポート期間タブのイベントリスナーの後に追加
    content = re.sub(
        r"(// レポート期間タブ\s*document\.querySelectorAll\('\.report-tab'\)\.forEach)",
        daily_pdf_code + "\n\n        \\1",
        content
    )
    
    # 出力
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 修正完了！")
    print(f"出力ファイル: {output_file}")
    print("\n修正内容:")
    print("  ①日付変更時間を0:00に修正")
    print("  ②契約先別集計の単価表示を修正")
    print("  ③作業履歴プルダウンを全件対応")
    print("  ④日別作業記録に稼働時間を表示")
    print("  ⑤日別作業PDF出力機能を追加")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使い方: python3 fix_html.py 元のファイル.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.html', '_fixed.html')
    
    try:
        fix_html(input_file, output_file)
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
