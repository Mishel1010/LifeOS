import streamlit as st
import pandas as pd
import calendar
import os
import json
import uuid
from datetime import datetime, date
import datetime as dt
from collections import OrderedDict
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import shutil
from streamlit_authenticator.utilities.hasher import Hasher
import re
from datetime import datetime, date, timedelta

st.markdown("""
    <style>
    /* 1. הסתרת כפתור הדיפלוי של סטרימליט ואת האייקונים של הלינקים האוטומטיים */
    [data-testid="stAppDeployButton"],
    button[data-testid="stHeaderDeployButton"],
    .stDeployButton,
    header[data-testid="stHeader"] div:has(button[data-testid="stAppDeployButton"]),
    a.aria-hidden,
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, .stMarkdown h4 a,
    h1 a, h2 a, h3 a, h4 a {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 2. הרחבת משטח העבודה הראשי באפליקציה ל-100% רוחב והקטנת שוליים */
    .appview-container .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1.5rem !important;
    }

    /* 3. מרכוז הכותרת הראשית בעמוד */
    .main-header {
        text-align: center !important;
        width: 100% !important;
        margin-bottom: 1.5rem !important;
    }

    /* 4. מיקום הלחצן הצף הכחול להוספת תנועה/עסקה */
    div[data-testid="stElementContainer"]:has(button[key="fab_btn"]),
    div[class*="st-key-fab_btn"] {
        position: fixed !important;
        bottom: 35px !important;
        right: 35px !important;
        z-index: 999999 !important;
        width: auto !important;
    }

    /* 5. עיצוב חזותי (צבע, צורה וצללית) של הלחצן הצף הכחול */
    div[data-testid="stElementContainer"]:has(button[key="fab_btn"]) button,
    div[class*="st-key-fab_btn"] button {
        background-color: #1976d2 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 14px 28px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        box-shadow: 0px 5px 18px rgba(0, 0, 0, 0.35) !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* 6. אפקט ריחוף על הלחצן הצף הכחול */
    div[data-testid="stElementContainer"]:has(button[key="fab_btn"]) button:hover,
    div[class*="st-key-fab_btn"] button:hover {
        background-color: #1565c0 !important;
        transform: scale(1.08) !important;
        box-shadow: 0px 8px 22px rgba(0, 0, 0, 0.45) !important;
        cursor: pointer !important;
    }

    /* 7. מיקום הלחצן הצף האדום להוספת קבוצת קטגוריות */
    div[data-testid="stElementContainer"]:has(button[key="fab_group_btn"]),
    div[class*="st-key-fab_group_btn"] {
        position: fixed !important;
        bottom: 100px !important; 
        right: 35px !important;
        z-index: 999998 !important;
        width: auto !important;
    }

    /* 8. עיצוב של הלחצן הצף האדום */
    div[data-testid="stElementContainer"]:has(button[key="fab_group_btn"]) button,
    div[class*="st-key-fab_group_btn"] button {
        background-color: #8e0000 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        box-shadow: 0px 5px 18px rgba(0, 0, 0, 0.35) !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* 9. אפקט ריחוף על הלחצן הצף האדום */
    div[data-testid="stElementContainer"]:has(button[key="fab_group_btn"]) button:hover,
    div[class*="st-key-fab_group_btn"] button:hover {
        background-color: #6d0000 !important;
        transform: scale(1.08) !important;
        box-shadow: 0px 8px 22px rgba(0, 0, 0, 0.45) !important;
        cursor: pointer !important;
    }

    /* 10. מיקום ומבנה קפסולת הניווט הצפה בתחתית המסך */
    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-btn_float_p"]) {
        position: fixed !important;
        bottom: 35px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 999999 !important;
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.3) !important;
        border-radius: 50px !important;
        padding: 4px 16px !important;
        box-shadow: 0px 5px 18px rgba(0, 0, 0, 0.35) !important;
        backdrop-filter: blur(8px) !important;
        width: max-content !important;
        height: 52px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 12px !important;
        box-sizing: border-box !important;
    }

    /* 11. התאמת רוחב ועמודות בתוך קפסולת הניווט הצפה */
    div[data-testid="stHorizontalBlock"]:has(div[class*="st-key-btn_float_p"]) > div[data-testid="stColumn"] {
        width: max-content !important;
        flex: 0 1 auto !important;
        min-width: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* 12. עיצוב חזותי של כפתורי החיצים בקפסולת הניווט */
    div[class*="st-key-btn_float_p"] button,
    div[class*="st-key-btn_float_n"] button {
        background-color: rgba(128, 128, 128, 0.15) !important;
        color: var(--text-color) !important;
        border-radius: 50% !important;
        width: 36px !important;
        height: 36px !important;
        min-height: 36px !important;
        max-height: 36px !important;
        padding: 0 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        border: 1px solid rgba(128, 128, 128, 0.25) !important;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.2s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* 13. אפקט ריחוף על כפתורי החיצים בקפסולת הניווט */
    div[class*="st-key-btn_float_p"] button:hover,
    div[class*="st-key-btn_float_n"] button:hover {
        background-color: rgba(128, 128, 128, 0.3) !important;
        transform: scale(1.1) !important;
        cursor: pointer !important;
        border-color: rgba(128, 128, 128, 0.4) !important;
    }  

    /* 14. איפוס רקע ומסגרת לכפתור תצוגת התאריך המרכזי בקפסולה */
    div[class*="st-key-date_dots_trigger"] button {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100% !important;
        width: 130px !important;
        cursor: pointer !important;
    }

    /* 15. אפקט ריחוף ומיקוד על כפתור תצוגת התאריך המרכזי */
    div[class*="st-key-date_dots_trigger"] button:hover,
    div[class*="st-key-date_dots_trigger"] button:focus,
    div[class*="st-key-date_dots_trigger"] button:active {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        transform: scale(1.02) !important;
    }

    /* 16. עיצוב הטקסט בתוך כפתור תצוגת התאריך המרכזי */
    div[class*="st-key-date_dots_trigger"] button p {
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        padding: 0 !important;
        color: var(--text-color) !important;
    }

    /* 17. שינוי צבע הטקסט בירוק בעת ריחוף על תצוגת התאריך המרכזי */
    div[class*="st-key-date_dots_trigger"] button:hover p {
        color: #2e7d32 !important;
    }

    /* 18. איפוס רקע ומסגרת לכפתור שלוש הנקודות בסרגל הצד */
    [data-testid="stSidebar"] div[class*="st-key-dots_"] button {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 38px !important;
        min-height: 38px !important;
        width: 100% !important;
        cursor: pointer !important;
    }

    /* 19. אפקט ריחוף והגדלה לכפתור שלוש הנקודות בסרגל הצד */
    [data-testid="stSidebar"] div[class*="st-key-dots_"] button:hover,
    [data-testid="stSidebar"] div[class*="st-key-dots_"] button:focus,
    [data-testid="stSidebar"] div[class*="st-key-dots_"] button:active {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        transform: scale(1.25) !important;
    }

    /* 20. עיצוב גודל כפתור שלוש הנקודות בסרגל הצד */
    [data-testid="stSidebar"] div[class*="st-key-dots_"] button p {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        margin: 0 !important;
        padding: 0 !important;
        color: var(--text-color) !important;
    }

    /* 21. שינוי צבע הטקסט בירוק בעת ריחוף על כפתור שלוש הנקודות */
    [data-testid="stSidebar"] div[class*="st-key-dots_"] button:hover p {
        color: #2e7d32 !important;
    }

    /* 22. הגדרת סמן יד ומעברים חלקים לשדות בחירה ולוחות שנה בתוך חלונות דיאלוג */
    div[role="dialog"] div[data-baseweb="select"] > div,
    div[role="dialog"] div[data-testid="stDateInput"] input,
    div[role="dialog"] div[data-baseweb="calendar"] button {
        cursor: pointer !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* 23. מסגרת ירוקה וצללית בריחוף על שדות בחירה ותאריכים בדיאלוגים */
    div[role="dialog"] div[data-baseweb="select"]:hover > div,
    div[role="dialog"] div[data-testid="stDateInput"]:hover input {
        border-color: #2e7d32 !important;
        box-shadow: 0 0 6px rgba(46, 125, 50, 0.3) !important;
    }

    /* 24. הגדרת סמן טקסט בשדות בתוך דיאלוגים */
    div[role="dialog"] div[data-testid="stTextInput"] input,
    div[role="dialog"] div[data-testid="stNumberInput"] input {
        cursor: text !important;
    }

    /* 25. מניעת אינטראקציה והעלמת חלוניות ה-Tooltip */
    div[data-testid="stTooltipContent"],
    div[data-baseweb="tooltip"] {
        pointer-events: none !important;
        transition: opacity 0.1s ease-in-out !important;
    }

    /* 26. עיצוב פס הכותרת האדום עבור אזור ההוצאות */
    .expenses-header-bar {
        background-color: #b71c1c !important;
        color: white !important;
        width: 100% !important;
        padding: 8px 0 !important;
        text-align: center !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        letter-spacing: 3px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
        margin-top: 1.8rem !important;
        margin-bottom: 1.2rem !important;
    }

    /* 27. עיצוב פס הכותרת הירוק עבור אזור ההכנסות */
    .income-header-bar {
        background-color: #2e7d32 !important;
        color: white !important;
        width: 100% !important;
        padding: 8px 0 !important;
        text-align: center !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        letter-spacing: 3px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
        margin-top: 1.8rem !important;
        margin-bottom: 1.2rem !important;
    }

    /* 28. עיצוב מסגרת, רקע ופינות מעוגלות לקוביות הקטגוריות בעמודות */
    div[data-testid="stColumn"] [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }

    
    /* 29. מרכוז הטקסט בתוך תוויות רכיבי הבחירה */
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stWidgetLabel"] p {
        text-align: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }

    /* 30. עיצוב גודל ומשקל הטקסט בכותרות קבוצות ההוצאות בלחיצה */
    div[data-testid="stColumn"] div[class*="st-key-group_title_btn_"] button p,
    div[data-testid="stColumn"] button[key^="group_title_btn_"] p {
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        text-align: center !important;
        width: 100% !important;
        margin: 0 !important;
        color: var(--text-color) !important;
    }
    
    /* 31. אפקט ריחוף והגדלה על כפתורי עריכת הכנסות/קטגוריות */
    div[class*="st-key-edit_inc_"] button:hover,
    div[class*="st-key-edit_cat_btn_"] button:hover {
        background-color: transparent !important;
        transform: scale(1.25) !important;
    }

    /* 32. התאמת מרווח אנכי לכפתור עריכת קטגוריה */
    div[class*="st-key-edit_cat_btn_"] {
        margin-top: -6px !important;
    }

    /* 33. עיצוב פס הכותרת של טבלת העסקאות */
    .transactions-header-bar {
        background-color: #808080 !important;
        color: white !important;
        width: 100% !important;
        padding: 8px 0 !important;
        text-align: center !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        letter-spacing: 3px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1) !important;
        margin-top: 1.8rem !important;
        margin-bottom: 1.2rem !important;
    }  

    /* 34. עיצוב מבנה שורת עסקאות בטבלה (ריווח ורוחב) */
    .tx-line {
        display: flex;
        align-items: center;
        padding: 17px 12px !important;
        border-radius: 6px;
        transition: background-color 0.2s ease;
        width: 100%;
        box-sizing: border-box !important;
    }
    
    /* 35. אפקט צבע רקע בעת ריחוף על שורת עסקה בטבלה */
    .tx-line:hover {
        background-color: rgba(128, 128, 128, 0.18) !important;
    }
    
    /* 36. אפקט ריחוף והגדלה לכפתורי עריכת עסקאות/הכנסות בטבלה */
    div[class*="st-key-edit_tx_inc_"] button:hover,
    div[class*="st-key-edit_tx_btn_"] button:hover {
        background-color: transparent !important;
        transform: scale(1.25) !important;
    }

    /* 37. עיצוב גודל, ריווח וצללית לתפריט הנפתח */
    div[data-testid="stPopoverBody"] {
        padding: 6px !important;
        min-width: 150px !important;
        width: 160px !important;
        border-radius: 10px !important;
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.25) !important;
    }


    /* 38. עיצוב לכפתורים בתוך התפריט הנפתח - ללא מסגרת */
    div[data-testid="stPopoverBody"] button {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        text-align: left !important;
        padding: 4px 8px !important;
        margin: 1px 0 !important;
        min-height: 28px !important;
        height: 32px !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: background-color 0.15s ease-in-out !important;
    }

    /* 39. אפקט ריחוף על כפתורים בתוך התפריט הנפתח */
    div[data-testid="stPopoverBody"] button:hover {
        background-color: rgba(128, 128, 128, 0.15) !important;
        transform: none !important;
    }

    /* 40. הוספת סמן יד ומעבר חלק לתיבות בחירה  */
    div[data-baseweb="select"] > div {
        cursor: pointer !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* 41. מסגרת כחולה וצללית בריחוף על תיבות בחירה */
    div[data-baseweb="select"]:hover > div {
        border-color: #1976d2 !important;
        box-shadow: 0 0 8px rgba(25, 118, 210, 0.25) !important;
    }
 
    /* 42. איפוס רקע ומסגרת לכפתור התאריך האמצעי בקפסולת החופשה */
    div[class*="st-key-vac_date_dots_trigger"] button {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        height: 0px !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
        cursor: pointer !important;
    }

    /* 43. אפקט הגדלה בריחוף על כפתור התאריך האמצעי בקפסולת החופשה */
    div[class*="st-key-vac_date_dots_trigger"] button:hover {
        transform: scale(1.05) !important;
    }

    /* 44. עיצוב הטקסט בכפתור התאריך האמצעי בקפסולת החופשה */
    div[class*="st-key-vac_date_dots_trigger"] button p {
        white-space: pre !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        color: var(--text-color) !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 45. עיצוב כפתור המדינה במסך החופשה */
    div[class*="st-key-pure_title_btn"] button {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 auto !important;
        height: auto !important;
        width: auto !important;
        min-height: unset !important;
        cursor: pointer !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* 46. אפקט ריחוף על כפתור בחירת המדינה */
    div[class*="st-key-pure_title_btn"] button:hover {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        transform: scale(1.02) !important;
    }

    /* 47. עיצוב הטקסט והגודל של כפתור כותרת המדינה והדגלים */
    div[class*="st-key-pure_title_btn"] button p {
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        color: var(--text-color) !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
        line-height: 1.1 !important;
    }

    /* 48. מיקום הלחצן הצף להוספת אטרקציה במודול החופשה */
    div[data-testid="stElementContainer"]:has(button[key="fab_attraction"]),
    div[class*="st-key-fab_attraction"] {
        position: fixed !important;
        bottom: 35px !important;
        right: 35px !important;
        z-index: 999999 !important;
        width: auto !important;
    }

    /* 49. עיצוב (צבע כחול, צורה וצללית) של הלחצן הצף להוספת אטרקציה */
    div[data-testid="stElementContainer"]:has(button[key="fab_attraction"]) button,
    div[class*="st-key-fab_attraction"] button {
        background-color: #1976d2 !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 14px 28px !important;
        height: 52px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        box-shadow: 0px 5px 18px rgba(0, 0, 0, 0.35) !important;
        border: none !important;
        transition: all 0.2s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
    }

    /* 50. אפקט ריחוף על הלחצן הצף להוספת אטרקציה */
    div[data-testid="stElementContainer"]:has(button[key="fab_attraction"]) button:hover,
    div[class*="st-key-fab_attraction"] button:hover {
        background-color: #1565c0 !important;
        transform: scale(1.08) !important;
        box-shadow: 0px 8px 22px rgba(0, 0, 0, 0.45) !important;
        cursor: pointer !important;
    }

    /* 51. איפוס ועיצוב כפתור כותרת המלון במודול החופשה - ללא מסגרת. */
    div[class*="st-key-hotel_title_btn_"] button {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 auto !important; 
        height: auto !important;
        width: 100% !important;
        text-align: center !important; 
        cursor: pointer !important;
        display: block !important;
    }

    /* 52. אפקט ריחוף על כפתור כותרת המלון */
    div[class*="st-key-hotel_title_btn_"] button:hover {
        background-color: transparent !important;
        transform: scale(1.01) !important;
    }

    /* 53. עיצוב הטקסט בתוך כפתור כותרת המלון - מודגש. */
    div[class*="st-key-hotel_title_btn_"] button p {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: var(--text-color) !important;
        margin: 0 auto !important;
        padding: 0 !important;
        text-align: center !important; 
    }

    /* 54. שינוי צבע הטקסט לכחול בריחוף על כפתור כותרת המלון */
    div[class*="st-key-hotel_title_btn_"] button:hover p {
        color: #1976d2 !important; 
    }

    /* 55. עיצוב כפתור המחיקה של ההערות */
    div[class*="st-key-del_"] button {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        min-height: auto !important;
        height: auto !important;
        color: #ff4b4b !important; 
        font-weight: bold !important;
        font-size: 0.85rem !important;
    }

    /* 56. אפקט ריחוף והגדלה על כפתור המחיקה של ההערות */
    div[class*="st-key-del_"] button:hover {
        background-color: transparent !important;
        transform: scale(1.15) !important; 
        color: #ff1a1a !important;
    }

    /* 57. הגדרת גודל וגובה לכפתורי עריכה כלליים */
    div[class*="st-key-edit_"] button {
        font-size: 0.5rem !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        height: 27px !important;
        min-height: 0px !important;
    }

    /* 58. עיצוב כפתורי אישור וביטול - ללא מסגרת. */
    div[class*="save_edit_"] button, div[class*="cancel_edit_"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        font-size: 1.1rem !important; 
        height: 68px !important; 
        width: 100% !important;
    }

    /* 59. עיצוב צבע כפתור ה-וי הירוק לשמירה */
    div[class*="save_edit_"] button {
        color: #28a745 !important;
        font-size: 0.1rem !important;
    }

    /* 60. עיצוב צבע כפתור האיקס האדום לביטול */
    div[class*="cancel_edit_"] button {
        color: #dc3545 !important;
        font-size: 0.1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.dialog("Delete Account")
def delete_user_dialog(username, config_data):
    st.warning("⚠️ Are you sure you want to delete your account? All your data and projects will be permanently deleted.")
    
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Yes, Delete", type="primary", use_container_width=True):
            if username in config_data['credentials']['usernames']:
                del config_data['credentials']['usernames'][username]
            
            with open('config.yaml', 'w', encoding='utf-8') as file:
                yaml.dump(config_data, file, allow_unicode=True, default_flow_style=False)
            
            user_folder = f"users_data/{username}"
            if os.path.exists(user_folder):
                shutil.rmtree(user_folder)
            
            st.session_state['authentication_status'] = None
            st.session_state['username'] = None
            st.session_state['name'] = None
            st.rerun()
            
    with col_no:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

@st.dialog("Edit User Profile")
def edit_user_profile_dialog(username, config_data):
    st.write(f"Editing profile for: **{username}**")
    
    user_info = config_data['credentials']['usernames'][username]
    current_email = user_info.get('email', '')
    current_name = user_info.get('name', '')
    
    with st.form("edit_user_profile_form"):
        new_username = st.text_input("Username", value=username)
        new_name = st.text_input("Full Name", value=current_name)
        new_email = st.text_input("Email", value=current_email)
        st.divider()
        st.markdown("**Change Password (leave blank to keep current):**")
        new_password = st.text_input("New Password", type="password")
        
        if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
            users_dict = config_data['credentials']['usernames']
            
            if new_username.strip() != username:
                if new_username.strip() in users_dict:
                    st.error("Username already exists. Please choose a different one.")
                    return
                else:
                    users_dict[new_username.strip()] = users_dict.pop(username)
                    old_folder = f"users_data/{username}"
                    new_folder = f"users_data/{new_username.strip()}"
                    if os.path.exists(old_folder):
                        os.rename(old_folder, new_folder)
                    username = new_username.strip()
                    st.session_state['username'] = username

            users_dict[username]['name'] = new_name.strip()
            users_dict[username]['email'] = new_email.strip()
            st.session_state['name'] = new_name.strip()
            
            if new_password.strip():
                hashed_pwd = Hasher().hash(new_password.strip())
                users_dict[username]['password'] = hashed_pwd
            
            with open('config.yaml', 'w', encoding='utf-8') as file:
                yaml.dump(config_data, file, allow_unicode=True, default_flow_style=False)
            
            st.success("Profile updated successfully!")
            st.rerun()

with open('config.yaml', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

query_params = st.query_params
url_user = query_params.get("logged_user", None)

if url_user and url_user in config['credentials']['usernames']:
    st.session_state['authentication_status'] = True
    st.session_state['username'] = url_user
    st.session_state['name'] = config['credentials']['usernames'][url_user].get('name', '')
else:
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

# בדיקת סטטוס ההתחברות
if st.session_state.get('authentication_status') == False:
    st.error("Incorrect username or password.")

elif st.session_state.get('authentication_status') == None:
    tab_login, tab_register = st.tabs(["LOG IN", "REGISTER"])
    
    with tab_login:
        st.write("Please enter your login details")

    with tab_register:
        st.write("Create a new account")
        with st.form("register_form"):
            reg_username = st.text_input("Username")
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            
            submit_register = st.form_submit_button("Register", type="primary")
            
            if submit_register:
                if reg_username and reg_name and reg_email and reg_password:
                    if reg_username in config['credentials']['usernames']:
                        st.error("Username already exists.")
                    else:
                        hashed_password = Hasher().hash(reg_password)
                        config['credentials']['usernames'][reg_username] = {
                            'email': reg_email, 'name': reg_name, 'password': hashed_password
                        }
                        with open('config.yaml', 'w', encoding='utf-8') as file:
                            yaml.dump(config, file, allow_unicode=True, default_flow_style=False)
                        os.makedirs(f"users_data/{reg_username}", exist_ok=True)
                        st.success("Registered successfully! Please go to log in.")
                else:
                    st.error("Please fill in all fields.")

elif st.session_state.get('authentication_status') == True:
    st.query_params["logged_user"] = st.session_state.get('username')

    with st.sidebar.popover(f"Hi, {st.session_state.get('name')} 😊"):
        
        # אופציה 1: עריכת משתמש
        if st.button("Edit Profile", use_container_width=True):
            edit_user_profile_dialog(st.session_state.get('username'), config)
            
        # אופציה 2: התנתקות
        if st.button("Log Out", use_container_width=True):
            try:
                authenticator.logout(location='unrendered')
            except Exception:
                pass
            
            st.session_state['authentication_status'] = None
            st.session_state['username'] = None
            st.session_state['name'] = None
            st.session_state['loaded_user'] = None
            
            if "logged_user" in st.query_params:
                del st.query_params["logged_user"]
            if "project" in st.query_params:
                del st.query_params["project"]
                
            st.rerun()
            
        # אופציה 3: מחיקת יוזר
        if st.button("Delete Account", use_container_width=True):
            delete_user_dialog(st.session_state.get('username'), config)

    current_username = st.session_state.get('username')
    user_data_dir = f"users_data/{current_username}"
    os.makedirs(user_data_dir, exist_ok=True)
    
    st.session_state.user_dir = user_data_dir
    st.session_state.projects_file = f"{user_data_dir}/projects.json"
    st.session_state.transactions_file = f"{user_data_dir}/transactions.csv"
    st.session_state.expense_cats_file = f"{user_data_dir}/expense_categories.json"
    st.session_state.income_cats_file = f"{user_data_dir}/income_categories.json"

    if st.session_state.get("loaded_user") != current_username:
        
        if os.path.exists(st.session_state.projects_file):
            with open(st.session_state.projects_file, "r", encoding="utf-8") as f:
                st.session_state.projects = json.load(f)
        else:
            st.session_state.projects = []

        st.session_state.loaded_user = current_username
        st.rerun()


    PROJECTS_FILE = f"{user_data_dir}/projects.json"
    transactions_file = f"{user_data_dir}/transactions.csv"
    income_cats_file = f"{user_data_dir}/income_categories.json"
    st.set_page_config(page_title="LifeOS", layout="wide")

    # ----------------------------------------------------
    # ניהול שמירה וטעינה של נתונים (JSON)
    # ----------------------------------------------------
    PROJECTS_FILE = "projects.json"

    MONTH_TO_NUM = {
        "January": 1, "February": 2, "March": 3, "April": 4, 
        "May": 5, "June": 6, "July": 7, "August": 8, 
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    NUM_TO_MONTH = {v: k for k, v in MONTH_TO_NUM.items()}

    def load_projects():
        path = st.session_state.projects_file
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_projects(projects):
        with open(st.session_state.projects_file, "w", encoding="utf-8") as f:
            json.dump(projects, f, ensure_ascii=False, indent=4)

    def delete_project_data(project_id):
        project_folder = f"{user_data_dir}/project_{project_id}"
        if os.path.exists(project_folder):
            shutil.rmtree(project_folder) # מוחק את התיקייה וכל הקבצים שבתוכה בפקודה אחת
            
        st.session_state.projects = [p for p in st.session_state.projects if p["id"] != project_id]
        save_projects(st.session_state.projects)
        if st.session_state.selected_project_id == project_id:
            st.session_state.selected_project_id = st.session_state.projects[0]["id"] if st.session_state.projects else None

    def load_expense_categories(cats_file):
        if os.path.exists(cats_file):
            with open(cats_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_expense_categories(cats_file, data):
        with open(cats_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def is_month_after_or_equal(m1, y1, m2, y2):
        if y1 > y2:
            return True
        elif y1 == y2:
            return MONTH_TO_NUM[m1] >= MONTH_TO_NUM[m2]
        return False

    if "projects" not in st.session_state:
        st.session_state.projects = load_projects()

    query_params = st.query_params
    url_project_id = query_params.get("project", None)

    if "selected_project_id" not in st.session_state:
        project_ids = [p["id"] for p in st.session_state.projects]
        if url_project_id in project_ids:
            st.session_state.selected_project_id = url_project_id
        else:
            st.session_state.selected_project_id = project_ids[0] if project_ids else None

    if st.session_state.selected_project_id:
        st.query_params["project"] = st.session_state.selected_project_id

    # ----------------------------------------------------
    # דיאלוגים 
    # ----------------------------------------------------
    @st.dialog("Create New Project")
    def add_project_dialog():
        project_type = st.selectbox(
            "Select Project Type:",
            ["Monthly Cash Flow Management", "Vacation Planner", "Hourly Wage Tracker", "Goal-Based Savings"]
        )
        project_name = st.text_input("Project Name:", value=f"My {project_type}")
        
        if st.button("Create Project", use_container_width=True, type="primary"):
            if project_name.strip():
                new_id = str(uuid.uuid4())
                new_project = {
                    "id": new_id,
                    "name": project_name.strip(),
                    "type": project_type
                }
                st.session_state.projects.append(new_project)
                save_projects(st.session_state.projects)
                st.session_state.selected_project_id = new_id
                st.rerun()
            else:
                st.error("Please enter a valid project name.")

    @st.dialog("Project Settings")
    def project_options_dialog(project_id, current_name):
        st.write("Edit project name or delete the project.")
        
        new_name = st.text_input("Project Name", value=current_name, key=f"dialog_input_{project_id}")
        
        st.write("")
        col_save, col_del = st.columns([0.6, 0.4])
        
        with col_save:
            if st.button("💾 Save Changes", type="primary", use_container_width=True):
                cleaned_new_name = new_name.strip()
                if cleaned_new_name:
                    for proj in st.session_state.projects:
                        if proj["id"] == project_id:
                            proj["name"] = cleaned_new_name
                            break
                    save_projects(st.session_state.projects)
                    st.rerun()
                else:
                    st.error("Project name cannot be empty.")

        with col_del:
            if st.button("🗑️ Delete Project", use_container_width=True):
                delete_project_data(project_id)
                st.rerun()

    @st.dialog("Add New Item")
    def unified_add_dialog(cats_file, income_cats_file, current_month, current_year):
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)
        
        add_type = st.selectbox(
            "What would you like to add?",
            ["Expense Category", "Income Category","Expense Category Group"]
        )
        
        st.divider()
        
        # אופציה 1: הוספת קבוצת קטגוריות הוצאה
        if add_type == "Expense Category Group":
            with st.form("form_add_group"):
                group_name = st.text_input("Group Name (e.g., Living Expenses, Entertainment, Vehicle)")
                
                if st.form_submit_button("Create Group", use_container_width=True, type="primary"):
                    if group_name.strip():
                        groups = load_expense_categories(cats_file)
                        g_name = group_name.strip()
                        if g_name not in groups:
                            groups[g_name] = {
                                "start_month": current_month,
                                "start_year": current_year,
                                "items": []
                            }
                            save_expense_categories(cats_file, groups)
                            st.success(f"Group '{g_name}' created!")
                            st.rerun()
                        else:
                            st.error("Group name already exists.")
                    else:
                        st.error("Please enter a group name.")
                        
        # אופציה 2: הוספת קטגוריית הוצאה תחת קבוצה קיימת
        elif add_type == "Expense Category":
            groups = load_expense_categories(cats_file)
            group_names = list(groups.keys())
            
            if not group_names:
                st.warning("Please create an Expense Category Group first!")
            else:
                with st.form("form_add_expense_item"):
                    selected_group = st.selectbox("Select Group:", group_names)
                    item_title = st.text_input("Category Name (e.g., Rent, Water, Electricity)")
                    budget = st.number_input("Monthly Budget (ILS)", value=None, placeholder="Enter Amount...", min_value=0.0, step=1.0)
                    is_recurring = st.radio("Frequency:", ["Recurring (Appears every month)", "One-time (This month only)"])
                    
                    if st.form_submit_button("Add Category", use_container_width=True, type="primary"):
                        if item_title.strip() and budget is not None and budget >= 0: 
                            new_item = {
                                "id": str(uuid.uuid4()),
                                "title": item_title.strip(),
                                "budget": budget,
                                "is_recurring": (is_recurring == "Recurring (Appears every month)"),
                                "created_month": current_month,
                                "created_year": current_year
                            }
                            groups[selected_group]["items"].append(new_item)
                            save_expense_categories(cats_file, groups)
                            st.success(f"Added '{item_title}' to {selected_group}!")
                            st.rerun()
                        else:
                            st.error("Please provide a valid name and budget amount.")

        # אופציה 3: הוספת קטגוריית הכנסה חדשה
        elif add_type == "Income Category":
            with st.form("form_add_income_cat"):
                cat_title = st.text_input("Income Source Name (e.g., Salary, Investments, Freelance)")
                budget = st.number_input("Planned Amount (ILS)", value=None, placeholder="Enter Amount...", min_value=0.0, step=1.0)
                is_recurring = st.radio("Frequency:", ["Recurring (Appears every month)", "One-time (This month only)"])
                
                if st.form_submit_button("Add Income Source", use_container_width=True, type="primary"):
                    if cat_title.strip() and budget is not None and budget >= 0:
                        if os.path.exists(income_cats_file):
                            with open(income_cats_file, "r", encoding="utf-8") as f:
                                income_data = json.load(f)
                        else:
                            income_data = {"items": []}
                        
                        new_item = {
                            "id": str(uuid.uuid4()),
                            "title": cat_title.strip(),
                            "budget": budget,
                            "is_recurring": (is_recurring == "Recurring (Appears every month)"),
                            "created_month": current_month,
                            "created_year": current_year
                        }
                        income_data["items"].append(new_item)
                        
                        with open(income_cats_file, "w", encoding="utf-8") as f:
                            json.dump(income_data, f, ensure_ascii=False, indent=4)
                            
                        st.success(f"Added income source '{cat_title}'!")
                        st.rerun()
                    else:
                        st.error("Please provide a valid name and amount.")

    @st.dialog("Add Expense Item")
    def add_item_dialog(cats_file, group_name, current_month, current_year):
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)
        st.write(f"Add item to group: **{group_name}**")
        
        item_title = st.text_input("Expense Name (e.g., Rent, Water, Electricity)")
        budget = st.number_input("Monthly Budget (ILS)", value=None, placeholder="Enter Amount...", min_value=0.0, step=1.0)
        is_recurring = st.radio("Frequency:", ["Recurring (Appears every month)", "One-time (This month only)"])
        
        if st.button("Add Item", use_container_width=True, type="primary"):
            if item_title.strip() and budget is not None and budget >= 0: 
                groups = load_expense_categories(cats_file)
                if group_name in groups:
                    new_item = {
                        "id": str(uuid.uuid4()),
                        "title": item_title.strip(),
                        "budget": budget,
                        "is_recurring": (is_recurring == "Recurring (Appears every month)"),
                        "created_month": current_month,
                        "created_year": current_year
                    }
                    groups[group_name]["items"].append(new_item)
                    save_expense_categories(cats_file, groups)
                    st.success(f"Added '{item_title}' to {group_name}!")
                    st.rerun()
            else:
                st.error("Please provide a valid title and budget amount.")

    @st.dialog("Edit Category")
    def edit_item_dialog(cats_file, group_name, item_data, current_month, current_year):
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)
        
        is_one_time_item = not item_data.get("is_recurring", True)
        
        with st.form(f"edit_expense_form_{item_data['id']}"):
            new_title = st.text_input("Category Name:", value=item_data["title"])
            new_budget = st.number_input(
                "Monthly Budget (ILS)", 
                value=float(item_data["budget"]), 
                min_value=0.0, 
                step=1.0
            )
            
            if is_one_time_item:
                update_mode = "This month only"
            else:
                update_mode = st.radio(
                    "Apply changes to:",
                    ["This month only", "From now on (Permanent)"]
                )
            
            col_save, col_del = st.columns(2)
            with col_save:
                if st.form_submit_button("Save Changes", use_container_width=True, type="primary"):
                    if new_title.strip() and new_budget >= 0:
                        groups = load_expense_categories(cats_file)
                        if group_name in groups:
                            for it in groups[group_name]["items"]:
                                if it["id"] == item_data["id"]:
                                    if update_mode == "From now on (Permanent)":
                                        months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                                        m_idx = months_list.index(current_month)
                                        if m_idx == 0:
                                            it["end_month"] = "December"
                                            it["end_year"] = int(current_year) - 1
                                        else:
                                            it["end_month"] = months_list[m_idx - 1]
                                            it["end_year"] = int(current_year)
                                        
                                        new_permanent_item = {
                                            "id": str(uuid.uuid4()),
                                            "title": new_title.strip(),
                                            "budget": new_budget,
                                            "is_recurring": True,
                                            "created_month": current_month,
                                            "created_year": int(current_year)
                                        }
                                        groups[group_name]["items"].append(new_permanent_item)
                                    else:
                                        if is_one_time_item:
                                            it["title"] = new_title.strip()
                                            it["budget"] = new_budget
                                        else:
                                            if "overrides" not in it:
                                                it["overrides"] = {}
                                            month_key = f"{current_month}_{current_year}"
                                            it["overrides"][month_key] = {
                                                "title": new_title.strip(),
                                                "budget": new_budget
                                            }
                                    break
                        
                        save_expense_categories(cats_file, groups)
                        st.rerun()
                    else:
                        st.error("Please enter a valid name and budget.")
                        
            with col_del:
                if st.form_submit_button("Delete Category", use_container_width=True):
                    groups = load_expense_categories(cats_file)
                    if group_name in groups:
                        for it in groups[group_name]["items"]:
                            if it["id"] == item_data["id"]:
                                months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                                m_idx = months_list.index(current_month)
                                if m_idx == 0:
                                    it["end_month"] = "December"
                                    it["end_year"] = int(current_year) - 1
                                else:
                                    it["end_month"] = months_list[m_idx - 1]
                                    it["end_year"] = int(current_year)
                                break
                                
                        save_expense_categories(cats_file, groups)
                        st.cache_data.clear()
                        st.rerun()

    @st.dialog("Edit Expense Group")
    def edit_group_dialog(cats_file, old_group_name):
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)
        st.write(f"Editing group: **{old_group_name}**")
        
        new_group_name = st.text_input("Group Name:", value=old_group_name)
        
        col_save, col_del = st.columns(2)
        with col_save:
            if st.button("Save Changes", use_container_width=True, type="primary"):
                new_name_clean = new_group_name.strip()
                if new_name_clean:
                    groups = load_expense_categories(cats_file)
                    if old_group_name in groups:
                        updated_groups = OrderedDict()
                        for k, v in groups.items():
                            if k == old_group_name:
                                updated_groups[new_name_clean] = v
                            else:
                                updated_groups[k] = v
                        
                        save_expense_categories(cats_file, updated_groups)
                        st.rerun()
                else:
                    st.error("Name cannot be empty.")
                    
        with col_del:
            if st.button("Delete Group", use_container_width=True):
                groups = load_expense_categories(cats_file)
                if old_group_name in groups:
                    del groups[old_group_name]
                    save_expense_categories(cats_file, groups)
                    st.rerun()

    months = list(MONTH_TO_NUM.keys())
    current_year = datetime.now().year
    years = list(range(2025, current_year + 50))

    if "select_month_box" not in st.session_state:
        st.session_state.select_month_box = months[datetime.now().month - 1]

    if "select_year_box" not in st.session_state:
        st.session_state.select_year_box = current_year if current_year in years else years[0]

    @st.dialog("Select Date")
    def open_date_dialog():
        new_month = st.selectbox("Month", months, index=months.index(st.session_state.select_month_box))
        new_year = st.selectbox("Year", years, index=years.index(int(st.session_state.select_year_box)))
        
        if st.button("Apply", type="primary", use_container_width=True):
            st.session_state.select_month_box = new_month
            st.session_state.select_year_box = new_year
            st.rerun()

    @st.dialog("Add Income Category")
    def add_income_category_dialog(income_cats_file, current_month, current_year):
        st.markdown('<div class="focus-tap" tabindex="0"></div>', unsafe_allow_html=True)
        with st.form("form_add_income_cat"):
            cat_title = st.text_input("Income Source Name (e.g., Salary, Investments, Freelance)")
            budget = st.number_input("Planned Amount (ILS)", value=None, placeholder="Enter Amount...", min_value=0.0, step=1.0)
            is_recurring = st.radio("Frequency:", ["Recurring (Appears every month)", "One-time (This month only)"])
            
            if st.form_submit_button("Add Income Source", use_container_width=True, type="primary"):
                if cat_title.strip() and budget is not None and budget >= 0:
                    
                    if os.path.exists(income_cats_file):
                        with open(income_cats_file, "r", encoding="utf-8") as f:
                            income_data = json.load(f)
                    else:
                        income_data = {"items": []}
                    
                    new_item = {
                        "id": str(uuid.uuid4()),
                        "title": cat_title.strip(),
                        "budget": budget,
                        "is_recurring": (is_recurring == "Recurring (Appears every month)"),
                        "created_month": current_month,
                        "created_year": current_year
                    }
                    income_data["items"].append(new_item)
                    
                    with open(income_cats_file, "w", encoding="utf-8") as f:
                        json.dump(income_data, f, ensure_ascii=False, indent=4)
                        
                    st.success(f"Added income source '{cat_title}'!")
                    st.rerun()
                else:
                    st.error("Please provide a valid name and amount.")

    @st.dialog("Edit Income Source")
    def edit_income_item_dialog(income_cats_file, item_data, current_month, current_year):
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)
        
        if os.path.exists(income_cats_file):
            with open(income_cats_file, "r", encoding="utf-8") as f:
                latest_data = json.load(f)
                for it in latest_data.get("items", []):
                    if it["id"] == item_data["id"]:
                        item_data = it
                        break

        with st.form(f"edit_income_form_{item_data['id']}_{current_month}"):
            new_title = st.text_input("Source Name:", value=item_data["title"])
            new_budget = st.number_input("Planned Amount (ILS):", value=float(item_data["budget"]), min_value=0.0, step=1.0)
            
            update_mode = st.radio(
                "Apply changes to:",
                ["From now on (Permanent)", "This month only"]
            )
            
            col_save, col_del = st.columns(2)
            with col_save:
                if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                    if new_title.strip() and new_budget >= 0:
                        
                        if os.path.exists(income_cats_file):
                            with open(income_cats_file, "r", encoding="utf-8") as f:
                                income_data = json.load(f)
                        else:
                            income_data = {"items": []}
                        
                        if update_mode == "From now on (Permanent)":
                            months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                            m_idx = months_list.index(current_month)
                            
                            for it in income_data["items"]:
                                if it["id"] == item_data["id"]:
                                    if m_idx == 0:
                                        it["end_month"] = "December"
                                        it["end_year"] = int(current_year) - 1
                                    else:
                                        it["end_month"] = months_list[m_idx - 1]
                                        it["end_year"] = int(current_year)
                                    break
                            
                            new_permanent_item = {
                                "id": str(uuid.uuid4()),
                                "title": new_title.strip(),
                                "budget": new_budget,
                                "is_recurring": True,
                                "created_month": current_month,
                                "created_year": int(current_year)
                            }
                            income_data["items"].append(new_permanent_item)

                        else:
                            for it in income_data["items"]:
                                if it["id"] == item_data["id"]:
                                    if "overrides" not in it:
                                        it["overrides"] = {}
                                    month_key = f"{current_month}_{current_year}"
                                    it["overrides"][month_key] = {
                                        "title": new_title.strip(),
                                        "budget": new_budget
                                    }
                                    break
                        
                        with open(income_cats_file, "w", encoding="utf-8") as f:
                            json.dump(income_data, f, ensure_ascii=False, indent=4)
                        
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Please provide a valid name and amount.")
                        
            with col_del:
                if st.form_submit_button("Delete Source", use_container_width=True):
                    if os.path.exists(income_cats_file):
                        with open(income_cats_file, "r", encoding="utf-8") as f:
                            income_data = json.load(f)
                    else:
                        income_data = {"items": []}
                    
                    for it in income_data.get("items", []):
                        if it["id"] == item_data["id"]:
                            months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                            m_idx = months_list.index(current_month)
                            if m_idx == 0:
                                it["end_month"] = "December"
                                it["end_year"] = int(current_year) - 1
                            else:
                                it["end_month"] = months_list[m_idx - 1]
                                it["end_year"] = int(current_year)
                            break
                    
                    with open(income_cats_file, "w", encoding="utf-8") as f:
                        json.dump(income_data, f, ensure_ascii=False, indent=4)
                    
                    st.cache_data.clear()
                    st.rerun()

    @st.dialog("Add New Transaction")
    def add_transaction_dialog(target_month, target_year, data_file, cats_file):
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)  
        st.write(f"Adding transaction (Default: **{target_month} {target_year}**)")

        if "tx_selected_date" not in st.session_state:
            try:
                default_m_num = MONTH_TO_NUM.get(target_month, datetime.now().month)
                st.session_state.tx_selected_date = date(int(target_year), default_m_num, min(datetime.now().day, 28))
            except:
                st.session_state.tx_selected_date = date.today()

        selected_date = st.date_input(
            "Select Date:", 
            value=st.session_state.tx_selected_date, 
            format="DD/MM/YYYY", 
            key="tx_date_picker",
            on_change=lambda: st.session_state.update({"tx_selected_date": st.session_state.tx_date_picker})
        )
        
        actual_month = NUM_TO_MONTH[selected_date.month]
        actual_year = int(selected_date.year)

        item_name = st.text_input("Description (e.g., Groceries, Salary, Entertainment)")
        amount = st.number_input("Amount (ILS)", value=None, placeholder="Enter Amount...", min_value=0.0, step=1.0)
        item_type = st.selectbox("Type:", ["Expense", "Income"])
        
        def get_sorting_key(title):
            clean_text = re.sub(r'^[^\w\s]+', '', title).strip()
            return clean_text.lower()
        
        if item_type == "Income":
            income_cats_file = f"{project_folder}/income_categories.json"           
            income_categories = []
            
            if os.path.exists(income_cats_file):
                with open(income_cats_file, "r", encoding="utf-8") as f:
                    inc_data = json.load(f)
                    
                    visible_inc_items = [
                        item for item in inc_data.get("items", [])
                        if (
                            (item["is_recurring"] and is_month_after_or_equal(actual_month, actual_year, item["created_month"], item["created_year"]))
                            or (not item["is_recurring"] and item["created_month"] == actual_month and item["created_year"] == actual_year)
                        ) and (
                            "end_month" not in item 
                            or is_month_after_or_equal(item["end_month"], item["end_year"], actual_month, actual_year)
                        )
                    ]
                    
                    for item in visible_inc_items:
                        month_key = f"{actual_month}_{actual_year}"
                        display_title = item["overrides"].get(month_key, {}).get("title", item["title"]) if "overrides" in item else item["title"]
                        if display_title not in income_categories:
                            income_categories.append(display_title)
            
            income_categories = sorted(income_categories, key=get_sorting_key)
            category = st.selectbox("Category:", income_categories if income_categories else ["General Income"])

        else:
            all_groups = load_expense_categories(cats_file)
            expense_categories = []
            
            for g_name, g_data in all_groups.items():
                if is_month_after_or_equal(actual_month, actual_year, g_data["start_month"], g_data["start_year"]):
                    
                    visible_items = [
                        item for item in g_data.get("items", [])
                        if (
                            (item.get("is_recurring", True) and is_month_after_or_equal(actual_month, actual_year, item["created_month"], item["created_year"]))
                            or (not item.get("is_recurring", True) and item["created_month"] == actual_month and int(item["created_year"]) == actual_year)
                        ) and (
                            "end_month" not in item 
                            or is_month_after_or_equal(item["end_month"], item["end_year"], actual_month, actual_year)
                        )
                    ]
                    
                    for item in visible_items:
                        month_key = f"{actual_month}_{actual_year}"
                        display_title = item["overrides"].get(month_key, {}).get("title", item["title"]) if "overrides" in item else item["title"]
                        
                        if display_title not in expense_categories:
                            expense_categories.append(display_title)
            
            expense_categories = sorted(expense_categories, key=get_sorting_key)
            category = st.selectbox("Category:", expense_categories if expense_categories else ["General Expense"])
        
        if st.button("Add Transaction", use_container_width=True, type="primary"):
            if item_name and amount is not None and amount > 0:
                chosen_day = int(selected_date.day)
                chosen_month_str = NUM_TO_MONTH[selected_date.month]
                chosen_year = int(selected_date.year)
                
                new_row = pd.DataFrame([{
                    "day": chosen_day,
                    "Description": item_name,
                    "Amount": amount,
                    "Type": item_type,
                    "Category": category,
                    "Month": chosen_month_str,
                    "Year": chosen_year
                }])
                
                st.session_state.financial_data = pd.concat([st.session_state.financial_data, new_row], ignore_index=True)
                st.session_state.financial_data.to_csv(data_file, index=False)
                st.success(f"Added successfully for {selected_date.strftime('%d/%m/%Y')}!")
                st.rerun()
            else:
                st.error("Please enter a valid description and amount.")

    @st.dialog("Edit Transaction")
    def edit_transaction_dialog(txs_file, tx_id, current_data, project_cats_file, income_cats_file):
        # שורת דמה ריקה למניעת בעיות פוקוס בחלונית
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)
        
        edit_state_key = f"edit_tx_date_{tx_id}"
        if edit_state_key not in st.session_state:
            curr_day = int(current_data["day"]) if "day" in current_data and pd.notna(current_data["day"]) else 1
            curr_month_str = str(current_data["Month"]) if "Month" in current_data else months[0]
            curr_year = int(current_data["Year"]) if "Year" in current_data else current_year
            
            curr_month_num = MONTH_TO_NUM.get(curr_month_str, 1)
            try:
                st.session_state[edit_state_key] = date(curr_year, curr_month_num, curr_day)
            except ValueError:
                st.session_state[edit_state_key] = date.today()

        fixed_type = str(current_data["Type"]) if "Type" in current_data else "Expense"
        curr_name = str(current_data["Description"]) if "Description" in current_data else ""
        curr_amt = float(current_data["Amount"]) if "Amount" in current_data and pd.notna(current_data["Amount"]) else 0.0

        selected_date = st.date_input(
            "Date", 
            value=st.session_state[edit_state_key], 
            format="DD/MM/YYYY",
            key=f"date_picker_{tx_id}",
            on_change=lambda: st.session_state.update({edit_state_key: st.session_state[f"date_picker_{tx_id}"]})
        )

        actual_month = NUM_TO_MONTH[selected_date.month]
        actual_year = int(selected_date.year)

        type_color = "#c62828" if fixed_type == "Expense" else "#2e7d32"

        st.markdown(f"<div style='margin-top: 4px; margin-bottom: 8px; font-weight: 500;'><b>Type:</b> <span style='color: {type_color}; font-weight: bold;'>{fixed_type}</span></div>", unsafe_allow_html=True)

        def get_sorting_key(title):
            clean_text = re.sub(r'^[^\w\s]+', '', str(title)).strip()
            return clean_text.lower()

        if fixed_type == "Income":
            available_categories = []
            if os.path.exists(income_cats_file):
                with open(income_cats_file, "r", encoding="utf-8") as f:
                    inc_data = json.load(f)
                    
                    visible_inc_items = [
                        item for item in inc_data.get("items", [])
                        if (
                            (item["is_recurring"] and is_month_after_or_equal(actual_month, actual_year, item["created_month"], item["created_year"]))
                            or (not item["is_recurring"] and item["created_month"] == actual_month and item["created_year"] == actual_year)
                        ) and (
                            "end_month" not in item 
                            or is_month_after_or_equal(item["end_month"], item["end_year"], actual_month, actual_year)
                        )
                    ]
                    
                    for item in visible_inc_items:
                        month_key = f"{actual_month}_{actual_year}"
                        display_title = item["overrides"].get(month_key, {}).get("title", item["title"]) if "overrides" in item else item["title"]
                        if display_title not in available_categories:
                            available_categories.append(display_title)
            
            available_categories = sorted(available_categories, key=get_sorting_key)
            if not available_categories:
                available_categories = ["General Income"]
        else:
            all_groups = load_expense_categories(project_cats_file)
            available_categories = []
            
            for g_name, g_data in all_groups.items():
                if is_month_after_or_equal(actual_month, actual_year, g_data["start_month"], g_data["start_year"]):
                    visible_items = [
                        item for item in g_data.get("items", [])
                        if (
                            (item.get("is_recurring", True) and is_month_after_or_equal(actual_month, actual_year, item["created_month"], item["created_year"]))
                            or (not item.get("is_recurring", True) and item["created_month"] == actual_month and int(item["created_year"]) == actual_year)
                        ) and (
                            "end_month" not in item 
                            or is_month_after_or_equal(item["end_month"], item["end_year"], actual_month, actual_year)
                        )
                    ]
                    
                    for item in visible_items:
                        month_key = f"{actual_month}_{actual_year}"
                        display_title = item["overrides"].get(month_key, {}).get("title", item["title"]) if "overrides" in item else item["title"]
                        if display_title not in available_categories:
                            available_categories.append(display_title)
            
            available_categories = sorted(available_categories, key=get_sorting_key)
            if not available_categories:
                available_categories = ["General Expense"]

        curr_cat = str(current_data["Category"]) if "Category" in current_data else available_categories[0]
        cat_index = available_categories.index(curr_cat) if curr_cat in available_categories else 0

        with st.form(f"edit_tx_form_{tx_id}"):
            new_cat = st.selectbox("Category", available_categories, index=cat_index)
            new_name = st.text_input("Description / Name", value=curr_name)
            new_amount = st.number_input("Amount (ILS)", value=curr_amt, min_value=0.0, step=0.01, format="%.2f")
            
            col_save, col_del = st.columns(2)
            with col_save:
                if st.form_submit_button("Save Changes", type="primary", use_container_width=True):
                    if new_name.strip() and new_amount >= 0:
                        df = pd.read_csv(txs_file)
                        if "ID" not in df.columns:
                            df["ID"] = range(len(df))
                        
                        chosen_day = int(selected_date.day)
                        chosen_month_str = NUM_TO_MONTH[selected_date.month]
                        chosen_year = int(selected_date.year)

                        mask = df["ID"] == tx_id
                        if mask.any():
                            df.loc[mask, "day"] = chosen_day
                            df.loc[mask, "Month"] = chosen_month_str
                            df.loc[mask, "Year"] = chosen_year
                            df.loc[mask, "Category"] = new_cat.strip()
                            df.loc[mask, "Description"] = new_name.strip()
                            df.loc[mask, "Amount"] = new_amount
                            df.to_csv(txs_file, index=False)
                        
                        if edit_state_key in st.session_state:
                            del st.session_state[edit_state_key]
                            
                        st.rerun()
                    else:
                        st.error("Please enter a valid description and amount.")
                        
            with col_del:
                if st.form_submit_button("Delete Transaction", use_container_width=True):
                    df = pd.read_csv(txs_file)
                    if "ID" not in df.columns:
                        df["ID"] = range(len(df))
                    
                    df = df[df["ID"] != tx_id]
                    df.to_csv(txs_file, index=False)
                    
                    if edit_state_key in st.session_state:
                        del st.session_state[edit_state_key]
                        
                    st.rerun()
    @st.dialog("📅 Jump to Day")
    def jump_to_day_dialog(trip_start, trip_end, vac_meta):
        if trip_start == trip_end:
            st.warning("It seems start and end dates are the same. Please edit them in settings.")
            
        total_days = (trip_end - trip_start).days + 1        
        for d in range(int(total_days)): 
            target_date = trip_start + dt.timedelta(days=d)
            d_num = d + 1
            date_str = target_date.strftime("%d/%m/%Y")
            
            if st.button(f"Day {d_num} — {date_str}", key=f"dialog_jump_{d_num}", use_container_width=True):
                vac_meta["current_trip_date"] = str(target_date)
                save_vacation_meta(vac_meta)
                st.rerun()

    @st.dialog("⚙️ Edit Trip Settings")
    def edit_trip_settings_dialog(vac_meta):
        current_start = datetime.strptime(vac_meta.get("start_date", str(date.today())), "%Y-%m-%d").date()
        current_end = datetime.strptime(vac_meta.get("end_date", str(date.today())), "%Y-%m-%d").date()
        current_travelers = int(vac_meta.get("travelers", 2))
        current_budget = float(vac_meta.get("budget", 10000.0))

        with st.form("edit_trip_form"):
            st.markdown("Update your trip logistics and dates:")
            
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                new_start = st.date_input("Start Date", value=current_start)
            with d_col2:
                new_end = st.date_input("End Date", value=current_end)

            t_col1, t_col2 = st.columns(2)
            with t_col1:
                new_travelers = st.number_input("Number of Travelers", min_value=1, value=current_travelers, step=1)
            with t_col2:
                new_budget = st.number_input("Total Budget (ILS)", min_value=0.0, value=current_budget, step=500.0)

            if st.form_submit_button("Save Changes 💾", use_container_width=True, type="primary"):
                vac_meta["start_date"] = str(new_start)
                vac_meta["end_date"] = str(new_end)
                vac_meta["travelers"] = new_travelers
                vac_meta["budget"] = new_budget
                
                curr_nav = datetime.strptime(vac_meta.get("current_trip_date", str(new_start)), "%Y-%m-%d").date()
                if curr_nav < new_start or curr_nav > new_end:
                    vac_meta["current_trip_date"] = str(new_start)

                save_vacation_meta(vac_meta)
                st.rerun()

    @st.dialog("➕ Add New Attraction")
    def add_attraction_dialog(v_meta, day_key):
        day_str = str(day_key)
        with st.form("add_attraction_form"):
            new_name = st.text_input("🎯 Attraction Name (e.g. Arakura Sengen Shrine)")
            
            c_time, c_dur = st.columns(2)
            start_time = c_time.time_input("Start Time", value=datetime.strptime("10:00:00", "%H:%M:%S").time())
            duration_hours = c_dur.number_input("Duration (Hours)", min_value=0.5, max_value=12.0, value=2.0, step=0.5)
            
            new_coords_str = st.text_input("📍 Google Maps Coordinates (e.g. 35.5013, 138.8023)")
            
            new_budget = st.number_input("💰 Budget (₪)", min_value=0, value=0, step=50)
            new_notes = st.text_area("📝 Notes")
            
            if st.form_submit_button("Add Attraction", use_container_width=True, type="primary"):
                if not new_name.strip():
                    st.error("Please enter an attraction name.")
                else:
                    new_item = {
                        "name": new_name,
                        "time": str(start_time),
                        "duration": duration_hours,
                        "coords": new_coords_str.strip(), 
                        "budget": new_budget,
                        "notes": new_notes
                    }
                    if "schedule" not in v_meta: v_meta["schedule"] = {}
                    if day_str not in v_meta["schedule"]: v_meta["schedule"][day_str] = []
                    
                    v_meta["schedule"][day_str].append(new_item)
                    save_vacation_meta(v_meta)
                    st.success("Added successfully!")
                    st.rerun()

    @st.dialog("✏️ Edit Attraction")
    def edit_attraction_dialog(v_meta, day_key, idx, item):
        day_str = str(day_key)
        with st.form(f"edit_attraction_form_{day_str}_{idx}"):
            new_name = st.text_input("🎯 Attraction Name", value=item.get('name', ''))
            
            c_time, c_dur = st.columns(2)
            try:
                def_time = datetime.strptime(item.get('time', '10:00:00'), "%H:%M:%S").time()
            except:
                def_time = datetime.strptime("10:00:00", "%H:%M:%S").time()

            start_time = c_time.time_input("Start Time", value=def_time)
            duration_hours = c_dur.number_input("Duration (Hours)", min_value=0.5, max_value=12.0, value=float(item.get('duration', 2.0)), step=0.5)
            
            new_coords_str = st.text_input("📍 Google Maps Coordinates", value=item.get('coords', ''))
            
            new_budget = st.number_input("💰 Budget (₪)", min_value=0, value=int(item.get('budget', 0)), step=50)
            new_notes = st.text_area("📝 Notes", value=item.get('notes', ''))
            
            col_save, col_del = st.columns(2)
            with col_save:
                if st.form_submit_button("Save Changes", use_container_width=True, type="primary"):
                    updated_item = {
                        "name": new_name,
                        "time": str(start_time),
                        "duration": duration_hours,
                        "coords": new_coords_str.strip(),
                        "budget": new_budget,
                        "notes": new_notes
                    }

                    if "schedule" not in v_meta: v_meta["schedule"] = {}
                    if day_str not in v_meta["schedule"]: v_meta["schedule"][day_str] = []

                    v_meta["schedule"][day_str][idx] = updated_item
                    save_vacation_meta(v_meta)
                    st.success("Updated successfully!")
                    st.rerun()
                    
            with col_del:
                if st.form_submit_button("Delete", use_container_width=True):
                    if day_str in v_meta.get("schedule", {}):
                        v_meta["schedule"][day_str].pop(idx)
                        save_vacation_meta(v_meta)
                        st.success("Deleted successfully!")
                        st.rerun()

    @st.dialog("🏨 Hotel Details & Dates")
    def hotel_details_dialog(v_meta, current_date, active_hotel):
        with st.form("hotel_form"):
            default_name = active_hotel.get("name", "") if active_hotel else ""
            default_address = active_hotel.get("address", "") if active_hotel else ""
            
            try:
                default_checkin = datetime.strptime(active_hotel["check_in"], "%Y-%m-%d").date() if active_hotel else current_date
                default_checkout = datetime.strptime(active_hotel["check_out"], "%Y-%m-%d").date() if active_hotel else current_date + timedelta(days=1)
            except:
                default_checkin = current_date
                default_checkout = current_date + timedelta(days=1)
                
            default_notes = active_hotel.get("notes", "") if active_hotel else ""

            hotel_name = st.text_input("Hotel Name", value=default_name)
            hotel_address = st.text_input("📍 Address / Location", value=default_address)
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                check_in = st.date_input("Check-in Date", value=default_checkin)
            with col_d2:
                check_out = st.date_input("Check-out Date", value=default_checkout)
                
            hotel_notes = st.text_area("📝 Hotel Notes (Booking ref, breakfast, etc.)", value=default_notes)
            
            if st.form_submit_button("Save Hotel Details", use_container_width=True, type="primary"):
                if "hotels" not in v_meta: 
                    v_meta["hotels"] = []
                
                new_hotel_data = {
                    "name": hotel_name,
                    "address": hotel_address,
                    "check_in": str(check_in),
                    "check_out": str(check_out),
                    "notes": hotel_notes
                }
                
                if active_hotel in v_meta["hotels"]:
                    v_meta["hotels"].remove(active_hotel)
                v_meta["hotels"].append(new_hotel_data)
                
                save_vacation_meta(v_meta)
                st.success("Hotel saved successfully!")
                st.rerun()

    
    # ----------------------------------------------------
    # סרגל צד - בחירת וניהול פרויקטים
    # ----------------------------------------------------
    st.sidebar.markdown("<h1 style='text-align: center; font-size: 2.2rem; font-weight: 800; letter-spacing: 2px;'>LifeOS</h1>", unsafe_allow_html=True)

    if st.sidebar.button("➕ Add New Project", use_container_width=True, type="primary"):
        add_project_dialog()

    if not st.session_state.projects:
        st.sidebar.info("No projects yet. Click 'Add New Project' to get started!")
        st.session_state.selected_project_id = None
    else:
        st.sidebar.subheader("Your Projects:", anchor=False)
        
        project_ids = [p["id"] for p in st.session_state.projects]
        if st.session_state.selected_project_id not in project_ids:
            st.session_state.selected_project_id = project_ids[0]

        for proj in st.session_state.projects:
            is_active = (proj["id"] == st.session_state.selected_project_id)
            
            icons = {
                "Monthly Cash Flow Management": "📊",
                "Vacation Planner": "✈️",
                "Hourly Wage Tracker": "💰",
                "Goal-Based Savings": "🎯"
            }
            icon = icons.get(proj["type"], "📁")
            
            clean_name = proj["name"]
            short_name = clean_name[:16] + "..." if len(clean_name) > 16 else clean_name
            
            col_icon, col_btn, col_3b = st.sidebar.columns([0.1, 0.78, 0.12], gap="small")
            
            with col_icon:
                st.markdown(f"<div style='text-align: center; font-size: 1.2rem; padding-top: 4px;'>{icon}</div>", unsafe_allow_html=True)
                
            with col_btn:
                btn_type = "primary" if is_active else "secondary"
                if st.button(
                    short_name, 
                    key=f"proj_btn_{proj['id']}", 
                    use_container_width=True,
                    type=btn_type,
                    help=clean_name
                ):
                    st.session_state.selected_project_id = proj["id"]
                    st.query_params["project"] = proj["id"]
                    st.rerun()

            with col_3b:
                if st.button("⋮", key=f"dots_{proj['id']}", help="Project Options"):
                    project_options_dialog(proj["id"], clean_name)
    st.sidebar.divider()

    # ----------------------------------------------------
    # במסך הראשי – המודול הנבחר
    # ----------------------------------------------------
    current_project = next(
        (p for p in st.session_state.projects if p["id"] == st.session_state.selected_project_id), 
        None
    )

    if current_project is None:
        st.markdown("""
            <div style='text-align: center; margin-top: 100px;'>
                <h2>Welcome to your life's operating system! 👋</h2>
                <p style='font-size: 1.2rem; color: #6c757d;'>You don't have any active projects yet.</p>
                <p style='font-size: 1.1rem;'>Click <b>➕ Add New Project</b> in the sidebar to create your first project!</p>
            </div>
        """, unsafe_allow_html=True)

    else:
        project_folder = f"{user_data_dir}/project_{current_project['id']}"
        os.makedirs(project_folder, exist_ok=True)

        # ------------------------------------------------
        # מודול 1: ניהול תזרים מזומנים
        # ------------------------------------------------
        if current_project["type"] == "Monthly Cash Flow Management":

            st.markdown(f"""
                <div class="main-header">
                    <h1 style='font-size: 3.5rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px;'>{current_project['name']}</h1>
                    <h3 style='color: #6c757d; font-weight: 400; margin-top: 5px;'>{current_project['type']}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            project_folder = f"{user_data_dir}/project_{current_project['id']}"
            os.makedirs(project_folder, exist_ok=True)
            
            project_data_file = f"{project_folder}/transactions.csv"
            project_cats_file = f"{project_folder}/expense_categories.json"
            income_cats_file = f"{project_folder}/income_categories.json"

            def load_project_data():
                if os.path.exists(project_data_file):
                    return pd.read_csv(project_data_file)
                return pd.DataFrame(columns=["day", "Description", "Amount", "Type", "Category", "Month", "Year"])

            st.session_state.financial_data = load_project_data()

            selected_month = st.session_state.select_month_box
            selected_year = st.session_state.select_year_box

            def prev_month_cb():
                curr_m_idx = months.index(st.session_state.select_month_box)
                curr_y_idx = years.index(st.session_state.select_year_box)
                if curr_m_idx > 0:
                    st.session_state.select_month_box = months[curr_m_idx - 1]
                elif curr_y_idx > 0:
                    st.session_state.select_month_box = months[11]
                    st.session_state.select_year_box = years[curr_y_idx - 1]

            def next_month_cb():
                curr_m_idx = months.index(st.session_state.select_month_box)
                curr_y_idx = years.index(st.session_state.select_year_box)
                if curr_m_idx < 11:
                    st.session_state.select_month_box = months[curr_m_idx + 1]
                elif curr_y_idx < len(years) - 1:
                    st.session_state.select_month_box = months[0]
                    st.session_state.select_year_box = years[curr_y_idx + 1]

            # ----------------------------------------------------
            # הנווט הצף בתחתית המסך
            # ----------------------------------------------------
            c_p, c_lbl, c_n = st.columns([1, 1, 1])
            with c_p:
                st.button("‹", key="btn_float_p", on_click=prev_month_cb, help="Previous Month")
            with c_lbl:
                if st.button(f"{selected_month} {selected_year}", key="date_dots_trigger", use_container_width=True, help="Click to change date"):
                    open_date_dialog()
            with c_n:
                st.button("›", key="btn_float_n", on_click=next_month_cb, help="Next Month")

            if st.button("➕ Add Transaction", key="fab_btn"):
                add_transaction_dialog(selected_month, selected_year, project_data_file, project_cats_file)

            all_df = st.session_state.financial_data
            if not all_df.empty:
                all_df["Year"] = all_df["Year"].astype(int)
                filtered_df = all_df[(all_df["Month"] == selected_month) & (all_df["Year"] == int(selected_year))]
            else:
                filtered_df = pd.DataFrame(columns=all_df.columns)

            #----------------------------------------------------
            # חישוב סיכום תזרים מזומנים
            #----------------------------------------------------

            all_groups = load_expense_categories(project_cats_file)
            total_planned_expenses = 0.0
            
            for g_name, g_data in all_groups.items():
                if is_month_after_or_equal(selected_month, int(selected_year), g_data["start_month"], g_data["start_year"]):
                    visible_items = [
                        item for item in g_data.get("items", [])
                        if (
                            (item.get("is_recurring", True) and is_month_after_or_equal(selected_month, int(selected_year), item["created_month"], item["created_year"]))
                            or (not item.get("is_recurring", True) and item["created_month"] == selected_month and int(item["created_year"]) == int(selected_year))
                        ) and (
                            "end_month" not in item 
                            or is_month_after_or_equal(item["end_month"], item["end_year"], selected_month, int(selected_year))
                        )
                    ]
                    total_planned_expenses += sum(
                        item["overrides"].get(f"{selected_month}_{selected_year}", {}).get("budget", item["budget"]) 
                        if "overrides" in item else item["budget"] 
                        for item in visible_items
                    )

            income_cats_file = f"{project_folder}/income_categories.json"
            income_groups_data = {"items": []}
            if os.path.exists(income_cats_file):
                with open(income_cats_file, "r", encoding="utf-8") as f:
                    income_groups_data = json.load(f)

            visible_income_items = [
                item for item in income_groups_data.get("items", [])
                if (
                    (
                        (item["is_recurring"] and is_month_after_or_equal(selected_month, int(selected_year), item["created_month"], item["created_year"]))
                        or (not item["is_recurring"] and item["created_month"] == selected_month and item["created_year"] == int(selected_year))
                    )
                    and (
                        "end_month" not in item 
                        or is_month_after_or_equal(item["end_month"], item["end_year"], selected_month, int(selected_year))
                    )
                )
            ]
            
            total_planned_income = sum(
                item["overrides"].get(f"{selected_month}_{selected_year}", {}).get("budget", item["budget"]) 
                if "overrides" in item else item["budget"] 
                for item in visible_income_items
            )

            planned_inc = total_planned_income  
            actual_inc = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
            
            planned_exp = total_planned_expenses  
            actual_exp = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
            
            planned_cf = planned_inc - planned_exp
            actual_cf = actual_inc - actual_exp
            col_inc, col_exp, col_cf = st.columns(3)

            with col_inc:
                st.markdown(f"""
                    <div style="border: 1px solid #e0e0e0; padding: 18px; border-radius: 10px; background-color: var(--secondary-background-color); color: var(--text-color); text-align: center;">
                        <h4 style="margin-top:0; color: #2e7d32;">Total Income</h4>
                        <hr style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; font-size: 1.1rem;">
                            <span><b>Planned:</b></span><span>₪{planned_inc:,.2f}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 1.1rem; margin-top: 8px;">
                            <span><b>Actual:</b></span><span style="color: #2e7d32; font-weight: bold;">₪{actual_inc:,.2f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col_exp:
                st.markdown(f"""
                    <div style="border: 1px solid #e0e0e0; padding: 18px; border-radius: 10px; background-color: var(--secondary-background-color); color: var(--text-color); text-align: center;">
                        <h4 style="margin-top:0; color: #c62828;">Total Expenses</h4>
                        <hr style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; font-size: 1.1rem;">
                            <span><b>Planned:</b></span><span>₪{planned_exp:,.2f}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 1.1rem; margin-top: 8px;">
                            <span><b>Actual:</b></span><span style="color: #c62828; font-weight: bold;">₪{actual_exp:,.2f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col_cf:
                st.markdown(f"""
                    <div style="border: 1px solid #e0e0e0; padding: 18px; border-radius: 10px; background-color: var(--secondary-background-color); color: var(--text-color); text-align: center;">
                        <h4 style="margin-top:0; color: #1565c0;">Cash Flow</h4>
                        <hr style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; font-size: 1.1rem;">
                            <span><b>Planned:</b></span><span>₪{planned_cf:,.2f}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; font-size: 1.1rem; margin-top: 8px;">
                            <span><b>Actual:</b></span><span style="color: #1565c0; font-weight: bold;">₪{actual_cf:,.2f}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # --------------------------------------------
            # בלוק הוצאות
            # --------------------------------------------
            st.markdown('<div class="expenses-header-bar">EXPENSES</div>', unsafe_allow_html=True)
            all_groups = load_expense_categories(project_cats_file)

            active_groups = {}
            for g_name, g_data in all_groups.items():
                if is_month_after_or_equal(selected_month, int(selected_year), g_data["start_month"], g_data["start_year"]):
                    active_groups[g_name] = g_data

            if "active_edit_item" in st.session_state and st.session_state.active_edit_item:
                edit_grp, edit_item = st.session_state.active_edit_item
                st.session_state.active_edit_item = None
                edit_item_dialog(project_cats_file, edit_grp, edit_item, selected_month, selected_year)

            if "active_edit_group" in st.session_state and st.session_state.active_edit_group:
                edit_grp_name = st.session_state.active_edit_group
                st.session_state.active_edit_group = None
                edit_group_dialog(project_cats_file, edit_grp_name)

            if not active_groups:
                st.info("No expense groups created yet. Click **'+ Add Category Group'** below to create your first group!")
            else:
                group_names = list(active_groups.keys())
                
                for i in range(0, len(group_names), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(group_names):
                            g_name = group_names[i + j]
                            g_data = active_groups[g_name]
                            
                            visible_items = [
                                item for item in g_data.get("items", [])
                                if (
                                    item.get("is_recurring", True) and is_month_after_or_equal(selected_month, int(selected_year), item["created_month"], item["created_year"])
                                ) or (
                                    not item.get("is_recurring", True) and item["created_month"] == selected_month and int(item["created_year"]) == int(selected_year)
                                )
                            ]
                            visible_items = [
                                item for item in visible_items
                                if (
                                    "end_month" not in item 
                                    or is_month_after_or_equal(item["end_month"], item["end_year"], selected_month, int(selected_year))
                                )
                            ]

                            import re
                            def get_sorting_key(title):
                                month_key = f"{selected_month}_{selected_year}"
                                display_title = title["overrides"].get(month_key, {}).get("title", title["title"]) if "overrides" in title else title["title"]
                                clean_text = re.sub(r'^[^\w\s]+', '', str(display_title)).strip()
                                return clean_text.lower()

                            visible_items = sorted(visible_items, key=get_sorting_key)

                            total_group_budget = sum(
                                item["overrides"].get(f"{selected_month}_{selected_year}", {}).get("budget", item["budget"]) 
                                if "overrides" in item else item["budget"] 
                                for item in visible_items
                            )

                            with cols[j]:
                                with st.container(border=True):
                                    if st.button(
                                        g_name, 
                                        key=f"group_title_btn_{g_name}_{selected_month}_{selected_year}", 
                                        use_container_width=True,
                                        help="Click to edit group name"
                                    ):
                                        st.session_state.active_edit_group = g_name
                                        st.rerun()

                                    st.markdown(f"<div style='text-align: center; color: var(--text-color); font-size: 0.85rem; margin-top: 4px;'>Total Budget: <b>₪{total_group_budget:,.2f}</b></div>", unsafe_allow_html=True)
                                    st.divider()

                                    if not visible_items:
                                        st.markdown("<div style='color: #a0a0a0; font-style: italic; padding: 6px 0; text-align: center;'>No items yet.</div>", unsafe_allow_html=True)
                                    else:
                                        for idx, item in enumerate(visible_items):
                                            month_key = f"{selected_month}_{selected_year}"
                                            display_title = item["overrides"].get(month_key, {}).get("title", item["title"]) if "overrides" in item else item["title"]
                                            display_budget = item["overrides"].get(month_key, {}).get("budget", item["budget"]) if "overrides" in item else item["budget"]

                                            actual_spent = 0.0
                                            if not filtered_df.empty:
                                                item_txs = filtered_df[
                                                    (filtered_df["Type"] == "Expense") & 
                                                    ((filtered_df["Category"] == display_title) | (filtered_df["Description"] == display_title))
                                                ]
                                                actual_spent = item_txs["Amount"].sum()

                                            x_color = "#2e7d32" if actual_spent <= display_budget else "#c62828"

                                            c_row, c_edit = st.columns([0.93, 0.07])
                                            
                                            with c_row:
                                                if display_budget == 0:
                                                    row_html = f"""
                                                    <div style='display: flex; justify-content: space-between; align-items: center; padding: 0px 0; font-size: 0.95rem; line-height: 0.8;'>
                                                        <span style='font-weight: 600; white-space: nowrap; padding-left: 4px;'> {display_title}</span>
                                                        <span style='flex-grow: 1; border-bottom: 2px dotted rgba(128, 128, 128, 0.3); margin: 0 8px;'></span>
                                                        <span style='font-weight: 700; white-space: nowrap;'>
                                                            <span style='color: var(--text-color);'>₪{actual_spent:,.0f}</span>
                                                        </span>
                                                    </div>
                                                    """
                                                else:
                                                    row_html = f"""
                                                    <div style='display: flex; justify-content: space-between; align-items: center; padding: 0px 0; font-size: 0.95rem; line-height: 0.8;'>
                                                        <span style='font-weight: 600; white-space: nowrap; padding-left: 4px;'> {display_title}</span>
                                                        <span style='flex-grow: 1; border-bottom: 2px dotted rgba(128, 128, 128, 0.3); margin: 0 8px;'></span>
                                                        <span style='font-weight: 700; white-space: nowrap;'>
                                                            <span style='color: {x_color};'>₪{actual_spent:,.0f}</span> / <span style='opacity: 0.8;'>₪{display_budget:,.0f}</span>
                                                        </span>
                                                    </div>
                                                    """
                                                st.markdown(row_html, unsafe_allow_html=True)

                                            with c_edit:
                                                if st.button("✏️", key=f"edit_cat_btn_exp_{g_name}_{item['id']}_{idx}_{selected_month}_{selected_year}", help="Edit Category"):
                                                    st.session_state.active_edit_item = (g_name, item)
                                                    st.rerun()

            if st.button("➕ Add Category/Group", key="fab_group_btn", help="Add Group or Category"):
                unified_add_dialog(project_cats_file, income_cats_file, selected_month, selected_year)

            # --------------------------------------------
            # בלוק ההכנסות 
            # --------------------------------------------
            st.markdown('<div class="income-header-bar">INCOME</div>', unsafe_allow_html=True)
            
            income_cats_file = f"{project_folder}/income_categories.json"
            
            if "active_edit_income_item" in st.session_state and st.session_state.active_edit_income_item:
                edit_inc_item = st.session_state.active_edit_income_item
                st.session_state.active_edit_income_item = None
                edit_income_item_dialog(income_cats_file, edit_inc_item, selected_month, selected_year)
            
            income_groups_data = {"items": []}
            if os.path.exists(income_cats_file):
                with open(income_cats_file, "r", encoding="utf-8") as f:
                    income_groups_data = json.load(f)

            visible_income_items = [
                item for item in income_groups_data.get("items", [])
                if (
                    (
                        (item["is_recurring"] and is_month_after_or_equal(selected_month, int(selected_year), item["created_month"], item["created_year"]))
                        or (not item["is_recurring"] and item["created_month"] == selected_month and item["created_year"] == int(selected_year))
                    )
                    and (
                        "end_month" not in item 
                        or is_month_after_or_equal(item["end_month"], item["end_year"], selected_month, int(selected_year))
                    )
                )
            ]

            import re
            def get_income_sorting_key(item):
                month_key = f"{selected_month}_{selected_year}"
                display_title = item["overrides"].get(month_key, {}).get("title", item["title"]) if "overrides" in item else item["title"]
                clean_text = re.sub(r'^[^\w\s]+', '', str(display_title)).strip()
                return clean_text.lower()

            visible_income_items = sorted(visible_income_items, key=get_income_sorting_key)

            total_planned_income = sum(
                item["overrides"].get(f"{selected_month}_{selected_year}", {}).get("budget", item["budget"]) 
                if "overrides" in item else item["budget"] 
                for item in visible_income_items
            )

            with st.container(border=True):
                if not visible_income_items:
                    st.markdown("<div style='color: #a0a0a0; font-style: italic; padding: 20px 0; text-align: center;'>No income sources added yet.</div>", unsafe_allow_html=True)
                else:
                    for idx, item in enumerate(visible_income_items):
                        month_key = f"{selected_month}_{selected_year}"
                        display_title = item["overrides"].get(month_key, {}).get("title", item["title"]) if "overrides" in item else item["title"]
                        display_budget = item["overrides"].get(month_key, {}).get("budget", item["budget"]) if "overrides" in item else item["budget"]

                        actual_income = 0.0
                        if not filtered_df.empty:
                            item_txs = filtered_df[
                                (filtered_df["Type"] == "Income") & 
                                ((filtered_df["Category"] == display_title) | (filtered_df["Description"] == display_title))
                            ]
                            actual_income = item_txs["Amount"].sum()

                        inc_color = "#2e7d32" if (actual_income > 0 and actual_income >= display_budget) else "var(--text-color)"               
                        c_row, c_btn = st.columns([0.975, 0.025])
                        
                        with c_row:
                            row_html = f"""
                            <div style='display: flex; justify-content: space-between; align-items: center; padding: 0px 0; font-size: 1.05rem; line-height: 2.7;'>
                                <span style='font-weight: 600; white-space: nowrap; padding-left: 8px;'> {display_title}</span>
                                <span style='flex-grow: 1; border-bottom: 2px dotted rgba(128, 128, 128, 0.3); margin: 0 5px;'></span>
                                <span style='font-weight: 700; white-space: nowrap;'>
                                    <span style='color: {inc_color};'>₪{actual_income:,.0f}</span> / <span style='opacity: 0.8;'>₪{display_budget:,.0f}</span>
                                </span>
                            </div>
                            """
                            st.markdown(row_html, unsafe_allow_html=True)
                        
                        with c_btn:
                            st.markdown(f"""
                                <div style='display: flex; align-items: center; justify-content: center; height: 100%;'>
                                    <div style='margin-top: -6px;'></div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("✏️", key=f"edit_cat_btn_inc_{item['id']}_{idx}_{selected_month}_{selected_year}", help="Edit Category"):
                                st.session_state.active_edit_income_item = item
                                st.rerun()

            # ------------------------------------------------------
            # בלוק טבלת התנועות החודשית 
            # ------------------------------------------------------

            st.markdown("""
            <style>
                
            </style>
            """, unsafe_allow_html=True)

            st.markdown(f"<div class='transactions-header-bar'>TRANSACTIONS — {selected_month} {selected_year}</div>", unsafe_allow_html=True)

            transactions_file = f"{project_folder}/transactions.csv"
            if os.path.exists(transactions_file):
                all_txs_df = pd.read_csv(transactions_file)
                
                if not all_txs_df.empty:
                    if "ID" not in all_txs_df.columns or all_txs_df["ID"].isna().any():   
                        all_txs_df["ID"] = range(len(all_txs_df))
                        all_txs_df.to_csv(transactions_file, index=False)

                    if "day" in all_txs_df.columns and "Month" in all_txs_df.columns and "Year" in all_txs_df.columns:
                        all_txs_df["TempDateStr"] = all_txs_df["day"].astype(str) + " " + all_txs_df["Month"].astype(str) + " " + all_txs_df["Year"].astype(str)
                        all_txs_df["ParsedDate"] = pd.to_datetime(all_txs_df["TempDateStr"], format="%d %B %Y", errors='coerce')
                    else:
                        all_txs_df["ParsedDate"] = pd.NaT

                    month_txs = all_txs_df[
                        (all_txs_df["Month"].astype(str).str.strip().str.lower() == selected_month.strip().lower()) & 
                        (all_txs_df["Year"].astype(int) == int(selected_year))
                    ].copy()
                    
                    month_txs = month_txs.sort_values(by="day", ascending=False)

                    if month_txs.empty:
                        st.info(f"No transactions recorded for {selected_month} {selected_year}.")
                    else:
                        _, table_col, _ = st.columns([0.15, 0.7, 0.15])
                        
                        with table_col:
                            with st.container(border=True):
                                hc_main, hc_edit_space = st.columns([0.96, 0.04])
                                with hc_main:
                                    st.markdown("""
                                    <div style='display: flex; align-items: center; width: 100%; padding: 4px 12px; margin-bottom: 12px;'>
                                        <div style='flex: 0.13; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>DATE</div>
                                        <div style='flex: 0.25; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>CATEGORY</div>
                                        <div style='flex: 0.44; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>DESCRIPTION</div>
                                        <div style='flex: 0.18; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>AMOUNT</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                st.markdown("<hr style='margin: 0px 0px 8px 0px; border-color: rgba(128, 128, 128, 0.2);'>", unsafe_allow_html=True)

                                row_to_edit = None
                                tx_id_to_edit = None

                                for idx, row in month_txs.iterrows():
                                    tx_day = int(row["day"]) if pd.notna(row["day"]) else 1
                                    tx_date = f"{tx_day:02d} {selected_month[:3]}"
                                    tx_name = str(row["Description"])
                                    tx_cat = str(row["Category"])
                                    tx_amt = float(row["Amount"])
                                    tx_id = int(row["ID"]) if pd.notna(row["ID"]) else idx
                                    is_income = row["Type"] == "Income"
                                    
                                    amt_color = "#2e7d32" if is_income else "#c62828"
                                    sign = "+" if is_income else "-"
                                
                                    t_row, p_row = st.columns([0.96, 0.04])
                                    
                                    with t_row:
                                        st.markdown(f"""
                                        <div class='tx-line' style='display: flex; align-items: center; width: 100%; padding: 10px 12px; margin-bottom: 4px;'>
                                            <div style='flex: 0.13; text-align: center; font-size: 0.9rem; font-weight: 500; opacity: 0.85;'>{tx_date}</div>
                                            <div style='flex: 0.25; text-align: center;'><span style='font-size: 0.8rem; opacity: 0.8; background: rgba(128, 128, 128, 0.15); padding: 3px 10px; border-radius: 12px; font-weight: 500;'>{tx_cat}</span></div>
                                            <div style='flex: 0.44; text-align: center; font-size: 0.95rem; font-weight: 600;'>{tx_name}</div>
                                            <div style='flex: 0.18; text-align: center; font-size: 0.95rem; font-weight: 700; color: {amt_color};'>{sign}₪{tx_amt:,.2f}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                    with p_row:
                                        st.markdown("<div class='edit-btn'>", unsafe_allow_html=True)
                                        if st.button("✏️", key=f"edit_tx_btn_{tx_id}_{selected_month}_{selected_year}", help="Edit Transaction"):
                                            row_to_edit = row
                                            tx_id_to_edit = tx_id
                                        st.markdown("</div>", unsafe_allow_html=True)
                                        
                                    st.markdown("<div style='border-bottom: 1px solid rgba(128, 128, 128, 0.1); margin: 0px 0;'></div>", unsafe_allow_html=True)

                                if row_to_edit is not None and tx_id_to_edit is not None:
                                    edit_transaction_dialog(transactions_file, tx_id_to_edit, row_to_edit, project_cats_file, income_cats_file)
                else:
                    st.info("Transactions file is empty.")
            else:
                st.info("No transactions file found.")

        # ------------------------------------------------
        # מודול 2: תכנון חופשה
        # ------------------------------------------------
        elif current_project["type"] == "Vacation Planner":
            vacation_folder = f"{project_folder}"
            os.makedirs(vacation_folder, exist_ok=True)
            
            vacation_meta_file = f"{vacation_folder}/vacation_meta.json"
            
            def load_vacation_meta():
                if os.path.exists(vacation_meta_file):
                    with open(vacation_meta_file, "r", encoding="utf-8") as f:
                        return json.load(f)
                return {}

            def save_vacation_meta(data):
                with open(vacation_meta_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            vac_meta = load_vacation_meta()

            countries_list = [
                "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
                "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
                "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia",
                "Denmark", "Djibouti", "Dominica", "Dominican Republic",
                "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia",
                "Fiji", "Finland", "France",
                "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
                "Haiti", "Honduras", "Hungary",
                "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
                "Jamaica", "Japan", "Jordan",
                "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
                "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
                "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
                "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway",
                "Oman",
                "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
                "Qatar",
                "Romania", "Russia", "Rwanda",
                "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
                "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu",
                "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
                "Vanuatu", "Vatican City", "Venezuela", "Vietnam",
                "Yemen",
                "Zambia", "Zimbabwe"
            ]

            country_emojis = {
                "Afghanistan": "🇦🇫", "Albania": "🇦🇱", "Algeria": "🇩🇿", "Andorra": "🇦🇩", "Angola": "🇦🇴", 
                "Antigua and Barbuda": "🇦🇬", "Argentina": "🇦🇷", "Armenia": "🇦🇲", "Australia": "🇦🇺", 
                "Austria": "🇦🇹", "Azerbaijan": "🇦🇿", "Bahamas": "🇧🇸", "Bahrain": "🇧🇭", "Bangladesh": "🇧🇩", 
                "Barbados": "🇧🇧", "Belarus": "🇧🇾", "Belgium": "🇧🇪", "Belize": "🇧🇿", "Benin": "🇧🇯", 
                "Bhutan": "🇧🇹", "Bolivia": "🇧🇴", "Bosnia and Herzegovina": "🇧🇦", "Botswana": "🇧🇼", 
                "Brazil": "🇧🇷", "Brunei": "🇧🇳", "Bulgaria": "🇧🇬", "Burkina Faso": "🇧🇫", "Burundi": "🇧🇮", 
                "Cabo Verde": "🇨🇻", "Cambodia": "🇰🇭", "Cameroon": "🇨🇲", "Canada": "🇨🇦", 
                "Central African Republic": "🇨🇫", "Chad": "🇹🇩", "Chile": "🇨🇱", "China": "🇨🇳", 
                "Colombia": "🇨🇴", "Comoros": "🇰🇲", "Congo": "🇨🇬", "Costa Rica": "🇨🇷", "Croatia": "🇭🇷", 
                "Cuba": "🇨🇺", "Cyprus": "🇨🇾", "Czechia": "🇨🇿", "Denmark": "🇩🇰", "Djibouti": "🇩🇯", 
                "Dominica": "🇩🇲", "Dominican Republic": "🇩🇴", "Ecuador": "🇪🇨", "Egypt": "🇪🇬", 
                "El Salvador": "🇸🇻", "Equatorial Guinea": "🇬🇶", "Eritrea": "🇪🇷", "Estonia": "🇪🇪", 
                "Eswatini": "🇸🇿", "Ethiopia": "🇪🇹", "Fiji": "🇫🇯", "Finland": "🇫🇮", "France": "🇫🇷", 
                "Gabon": "🇬🇦", "Gambia": "🇬🇲", "Georgia": "🇬🇪", "Germany": "🇩🇪", "Ghana": "🇬🇭", 
                "Greece": "🇬🇷", "Grenada": "🇬🇩", "Guatemala": "🇬🇹", "Guinea": "🇬🇳", "Guinea-Bissau": "🇬🇼", 
                "Guyana": "🇬🇾", "Haiti": "🇭🇹", "Honduras": "🇭🇳", "Hungary": "🇭🇺", "Iceland": "🇮🇸", 
                "India": "🇮🇳", "Indonesia": "🇮🇩", "Iran": "🇮🇷", "Iraq": "🇮🇶", "Ireland": "🇮🇪", 
                "Israel": "🇮🇱", "Italy": "🇮🇹", "Jamaica": "🇯🇲", "Japan": "🇯🇵", "Jordan": "🇯🇴", 
                "Kazakhstan": "🇰🇿", "Kenya": "🇰🇪", "Kiribati": "🇰🇮", "Kuwait": "🇰🇼", "Kyrgyzstan": "🇰🇬", 
                "Laos": "🇱🇦", "Latvia": "🇱🇻", "Lebanon": "🇱🇧", "Lesotho": "🇱🇸", "Liberia": "🇱🇷", 
                "Libya": "🇱🇾", "Liechtenstein": "🇱🇮", "Lithuania": "🇱🇹", "Luxembourg": "🇱🇺", 
                "Madagascar": "🇲🇬", "Malawi": "🇲🇼", "Malaysia": "🇲🇾", "Maldives": "🇲🇻", "Mali": "🇲🇱", 
                "Malta": "🇲🇹", "Marshall Islands": "🇲🇭", "Mauritania": "🇲🇷", "Mauritius": "🇲🇺", 
                "Mexico": "🇲🇽", "Micronesia": "🇫🇲", "Moldova": "🇲🇩", "Monaco": "🇲🇨", "Mongolia": "🇲🇳", 
                "Montenegro": "🇲🇪", "Morocco": "🇲🇦", "Mozambique": "🇲🇿", "Myanmar": "🇲🇲", "Namibia": "🇳🇦", 
                "Nauru": "🇳🇷", "Nepal": "🇳🇵", "Netherlands": "🇳🇱", "New Zealand": "🇳🇿", "Nicaragua": "🇳🇮", 
                "Niger": "🇳🇪", "Nigeria": "🇳🇬", "North Korea": "🇰🇵", "North Macedonia": "🇲🇰", "Norway": "🇳🇴", 
                "Oman": "🇴🇲", "Pakistan": "🇵🇰", "Palau": "🇵🇼", "Palestine": "🇵🇸", "Panama": "🇵🇦", 
                "Papua New Guinea": "🇵🇬", "Paraguay": "🇵🇾", "Peru": "🇵🇪", "Philippines": "🇵🇭", 
                "Poland": "🇵🇱", "Portugal": "🇵🇹", "Qatar": "🇶🇦", "Romania": "🇷🇴", "Russia": "🇷🇺", 
                "Rwanda": "🇷🇼", "Saint Kitts and Nevis": "🇰🇳", "Saint Lucia": "🇱🇨", 
                "Saint Vincent and the Grenadines": "🇻🇨", "Samoa": "🇼🇸", "San Marino": "🇸🇲", 
                "Sao Tome and Principe": "🇸🇹", "Saudi Arabia": "🇸🇦", "Senegal": "🇸🇳", "Serbia": "🇷🇸", 
                "Seychelles": "🇸🇨", "Sierra Leone": "🇸🇱", "Singapore": "🇸🇬", "Slovakia": "🇸🇰", 
                "Slovenia": "🇸🇮", "Solomon Islands": "🇸🇧", "Somalia": "🇸🇴", "South Africa": "🇿🇦", 
                "South Korea": "🇰🇷", "South Sudan": "🇸🇸", "Spain": "🇪🇸", "Sri Lanka": "🇱🇰", 
                "Sudan": "🇸🇩", "Suriname": "🇸🇷", "Sweden": "🇸🇪", "Switzerland": "🇨🇭", "Syria": "🇸🇾", 
                "Taiwan": "🇹🇼", "Tajikistan": "🇹🇯", "Tanzania": "🇹🇿", "Thailand": "🇹🇭", "Timor-Leste": "🇹🇱", 
                "Togo": "🇹🇬", "Tonga": "🇹🇴", "Trinidad and Tobago": "🇹🇹", "Tunisia": "🇹🇳", "Turkey": "🇹🇷", 
                "Turkmenistan": "🇹🇲", "Tuvalu": "🇹🇻", "Uganda": "🇺🇬", "Ukraine": "🇺🇦", 
                "United Arab Emirates": "🇦🇪", "United Kingdom": "🇬🇧", "United States": "🇺🇸", 
                "Uruguay": "🇺🇾", "Uzbekistan": "🇺🇿", "Vanuatu": "🇻🇺", "Vatican City": "🇻🇦", 
                "Venezuela": "🇻🇪", "Vietnam": "🇻🇳", "Yemen": "🇾🇪", "Zambia": "🇿🇲", "Zimbabwe": "🇿🇼"
            }

            countries_with_placeholder = ["Select Country..."] + countries_list
            selected_country = vac_meta.get("country", "Select Country...")

            if selected_country == "Select Country...":
                st.markdown("""
                    <div style='text-align: center; margin-top: 40px; margin-bottom: 30px;'>
                        <h2 style='font-size: 2.8rem; font-weight: 800;'>✈️ Planning a New Adventure? 🌴</h2>
                        <p style='font-size: 1.2rem; color: #6c757d;'>Select your destination and let's build the ultimate itinerary.</p>
                    </div>
                """, unsafe_allow_html=True)

                col_space1, col_center, col_space2 = st.columns([1, 2, 1])
                with col_center:
                    chosen_country = st.selectbox(
                        "Where are we flying to?",
                        options=countries_with_placeholder,
                        index=0,
                        key=f"country_select_{current_project['id']}"
                    )
                    
                    st.write("")
                    if st.button("Set Destination & Continue 🚀", use_container_width=True, type="primary"):
                        if chosen_country == "Select Country...":
                            st.error("Please select a valid destination country first.")
                        else:
                            vac_meta["country"] = chosen_country
                            save_vacation_meta(vac_meta)
                            st.rerun()

            elif "start_date" not in vac_meta or "end_date" not in vac_meta:
                flag_emoji = country_emojis.get(selected_country, "🌍")

                st.markdown(f"""
                    <div style='text-align: center; margin-top: 20px; margin-bottom: 30px;'>
                        <div style='font-size: 10rem; line-height: 1; margin-bottom: 15px;'>{flag_emoji}</div>
                        <h1 style='margin: 0; font-size: 4.5rem; font-weight: 900; letter-spacing: 3px;'>{selected_country.upper()}</h1>
                    </div>
                """, unsafe_allow_html=True)

                col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
                with col_b2:
                    if st.button("🔄 Change Country", use_container_width=True, type="secondary"):
                        vac_meta["country"] = "Select Country..."
                        save_vacation_meta(vac_meta)
                        st.rerun()

                st.divider()

                st.markdown("<h4 style='margin-bottom: 15px; text-align: center;'>Trip Parameters & Logistics</h4>", unsafe_allow_html=True)

                with st.form(f"vacation_details_form_{current_project['id']}"):
                    col_dates1, col_dates2 = st.columns(2)
                    with col_dates1:
                        start_date = st.date_input("Start Date", value=date.today())
                    with col_dates2:
                        end_date = st.date_input("End Date", value=date.today())

                    col_det1, col_det2 = st.columns(2)
                    with col_det1:
                        travelers_count = st.number_input("Number of Travelers", min_value=1, value=2, step=1)
                    with col_det2:
                        total_budget = st.number_input("Total Budget (ILS)", min_value=0.0, value=10000.0, step=500.0)

                    if st.form_submit_button("Save Vacation Settings & Open Itinerary 🚀", use_container_width=True, type="primary"):
                        vac_meta["start_date"] = str(start_date)
                        vac_meta["end_date"] = str(end_date)
                        vac_meta["travelers"] = travelers_count
                        vac_meta["budget"] = total_budget
                        vac_meta["current_trip_date"] = str(start_date)
                        save_vacation_meta(vac_meta)
                        st.rerun()

            else:
                flag_emoji = country_emojis.get(selected_country, "🌍")

                col_c1, col_c2, col_c3 = st.columns([1, 4, 1])
                with col_c2:
                    if st.button(f"{flag_emoji}  {selected_country.upper()}  {flag_emoji}", key="pure_title_btn", use_container_width=True, help="Click to edit trip settings"):
                        edit_trip_settings_dialog(vac_meta)

                st.divider()
                
                trip_start = datetime.strptime(vac_meta["start_date"], "%Y-%m-%d").date()
                trip_end = datetime.strptime(vac_meta["end_date"], "%Y-%m-%d").date()

                if "current_trip_date" not in vac_meta or not vac_meta["current_trip_date"]:
                    vac_meta["current_trip_date"] = str(trip_start)
                    save_vacation_meta(vac_meta)

                current_nav_date = datetime.strptime(vac_meta["current_trip_date"], "%Y-%m-%d").date()

                if current_nav_date < trip_start:
                    current_nav_date = trip_start
                elif current_nav_date > trip_end:
                    current_nav_date = trip_end

                day_number = (current_nav_date - trip_start).days + 1

                def prev_day_cb():
                    prev_d = current_nav_date - dt.timedelta(days=1)
                    if prev_d >= trip_start:
                        vac_meta["current_trip_date"] = str(prev_d)
                        save_vacation_meta(vac_meta)

                def next_day_cb():
                    next_d = current_nav_date + dt.timedelta(days=1)
                    if next_d <= trip_end:
                        vac_meta["current_trip_date"] = str(next_d)
                        save_vacation_meta(vac_meta)

                #-------------------------------------------------
                # נווט צף בתחתית המסך
                #-------------------------------------------------

                c_p, c_lbl, c_n = st.columns([1, 1.4, 1])
                with c_p:
                    st.button("‹", key="btn_float_p", on_click=prev_day_cb, help="Previous Day")
                with c_lbl:
                    date_formatted = current_nav_date.strftime("%d/%m/%Y")
                    if st.button(f"Day {day_number}\n{date_formatted}", key="vac_date_dots_trigger", use_container_width=True, help="Click to select a day"):
                        jump_to_day_dialog(trip_start, trip_end, vac_meta)
                with c_n:
                    st.button("›", key="btn_float_n", on_click=next_day_cb, help="Next Day")
            
                current_day_key = str(current_nav_date)
                
                if "schedule" not in vac_meta: vac_meta["schedule"] = {}
                if current_day_key not in vac_meta["schedule"]: vac_meta["schedule"][current_day_key] = []

                if "days_metadata" not in vac_meta: vac_meta["days_metadata"] = {}
                if current_day_key not in vac_meta["days_metadata"]:
                    vac_meta["days_metadata"][current_day_key] = {
                        "hotel": "",
                        "wake_up": "08:00",
                        "notes": ""
                    }

                current_day_meta = vac_meta["days_metadata"][current_day_key]
                day_schedule = vac_meta["schedule"][current_day_key]

                col_schedule, col_overview = st.columns([1.3, 1], gap="large")

                #------------------------------------------
                # צד שמאל: Schedule
                #------------------------------------------

                with col_schedule:
                    st.markdown("### 🕒 Schedule")
                    
                    if not day_schedule:
                        st.info("No attractions added for this day yet. Click the button on the bottom right to add.")
                    else:
                        day_schedule.sort(key=lambda x: x['time'])
                        
                        st.markdown("""
                        <style>
                            .attr-card-row {
                                display: flex;
                                align-items: center;
                                justify-content: space-between;
                                width: 100%;
                            }
                            .attr-time-col {
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                min-width: 90px;
                            }
                            .attr-start-time {
                                font-size: 1.1rem;
                                font-weight: 800;
                                line-height: 1;
                            }
                            .attr-duration {
                                font-size: 0.75rem;
                                opacity: 0.75;
                                border-left: 2px dotted rgba(128, 128, 128, 0.6);
                                padding-left: 6px;
                                margin-top: 10px;
                                margin-bottom: 10px;
                                line-height: 1.5;
                            }
                            .attr-info-col {
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                                flex-grow: 1;
                                padding: 0 20px;
                            }
                            .attr-name {
                                font-size: 1.05rem;
                                font-weight: 700;
                                line-height: 1.5;
                                margin-top: 0px;
                                margin-bottom: 3px;
                            }
                            .attr-loc {
                                font-size: 0.8rem;
                                opacity: 0.75;
                                margin-top: 3px;
                                margin-bottom: 15px;
                            }
                            .attr-budget-col {
                                font-size: 1.05rem;
                                font-weight: 800;
                                white-space: nowrap;
                                padding-right: 10px;
                                margin-top: 10px;
                                margin-bottom: 29px;
                            }
                            div[class*="st-key-edit_attr_"] {
                                display: flex !important;
                                align-items: center !important;
                                justify-content: center !important;
                                height: 100% !important;
                            }
                            div[class*="st-key-edit_attr_"] button {
                                background: transparent !important;
                                border: none !important;
                                box-shadow: none !important;
                                padding: 0 !important;
                                font-size: 1.1rem !important;
                                min-height: unset !important;
                                height: auto !important;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        for idx, item in enumerate(day_schedule):
                            with st.container(border=True):
                                c_content, c_edit = st.columns([0.93, 0.07], vertical_alignment="center")
                                
                                start_time_str = item['time'][:5]
                                duration_val = item.get('duration', 0)
                                loc_display = item.get('coords', item.get('location', ''))
                                
                                with c_content:
                                    st.markdown(f"""
                                        <div class="attr-card-row">
                                            <div class="attr-time-col">
                                                <span class="attr-start-time">{start_time_str}</span>
                                                <div class="attr-duration">Duration:<br><b>{duration_val} hrs</b></div>
                                            </div>
                                            <div class="attr-info-col">
                                                <div class="attr-name">{item.get('name')}</div>
                                                <div class="attr-loc">{loc_display}</div>
                                            </div>
                                            <div class="attr-budget-col">₪{item.get('budget', 0)}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                                
                                with c_edit:
                                    if st.button("✏️", key=f"edit_attr_{current_day_key}_{idx}", help="Edit Attraction"):
                                        edit_attraction_dialog(vac_meta, current_day_key, idx, item)

                #------------------------------------------
                # צד ימין: Day Overview
                #------------------------------------------
                with col_overview:
                    st.markdown("### 📋 Day Overview")
                    
                    row1_c1, row1_c2 = st.columns(2)

                    #========== תקציב ============

                    with row1_c1:
                        total_daily_budget = sum(item['budget'] for item in day_schedule)
                        with st.container(border=True):
                            st.markdown("<div style='text-align: center; font-size: 1.5rem;'><strong>💰 Daily Budget</strong></div>", unsafe_allow_html=True)
                            st.markdown(f"<h2 style='text-align: center; margin: 6px 0 0 0; font-weight: 800;'>₪{total_daily_budget}</h2>", unsafe_allow_html=True)
                            st.caption("Total cost of today's spots")

                    #========= בית מלון ===========
                    with row1_c2:
                        hotels_list = vac_meta.get("hotels", [])
                        active_hotel = None
                        for h in hotels_list:
                            if h["check_in"] <= current_day_key < h["check_out"]:
                                active_hotel = h
                                break

                        with st.container(border=True):
                            if active_hotel:
                                if st.button(f"🏨 {active_hotel['name']}", key=f"hotel_title_btn_{current_day_key}", help="Click to edit hotel details"):
                                    hotel_details_dialog(vac_meta, current_nav_date, active_hotel)
                                
                                st.markdown(f"<small>📅 <b>{active_hotel['check_in']}</b> ➔ <b>{active_hotel['check_out']}</b></small>", unsafe_allow_html=True)
                                
                                st.markdown(f"📍 {active_hotel['address']}")
                                if active_hotel.get('notes'):
                                    st.caption(f"📝 {active_hotel['notes']}")
                            else:
                                st.markdown("#### 🏨 Hotel Stay")
                                st.info("No hotel set for today.")
                                
                                st.write("")
                                if st.button("➕ Add Hotel Details", key=f"hotel_card_add_{current_day_key}", use_container_width=True, type="primary"):
                                    hotel_details_dialog(vac_meta, current_nav_date, None)

                    row2_c1, row2_c2 = st.columns(2)

                    st.markdown("""
                    <style>
                        /* מוצא את שתי הקוביות הראשונות בתוך השורה התחתונה ומוודא שגובהן אחיד */
                        div[data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"],
                        div[data-testid="column"]:nth-of-type(2) div[data-testid="stVerticalBlockBorderWrapper"] {
                            height: 100% !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)

                    #=============== הערות ==============
                    with row2_c1:
                        st.markdown("""
                        <style>
                            div[data-testid="stTextArea"] textarea {
                                font-size: 0.85rem !important;
                                min-height: 68px !important;
                                padding: 2px 2px !important;
                                resize: vertical !important;
                            }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📝 Daily Notes", expanded=False):
                            
                            if "days_metadata" not in vac_meta: vac_meta["days_metadata"] = {}
                            if current_day_key not in vac_meta["days_metadata"]: vac_meta["days_metadata"][current_day_key] = {}
                            if "notes_list" not in vac_meta["days_metadata"][current_day_key]:
                                vac_meta["days_metadata"][current_day_key]["notes_list"] = []
                            
                            notes_list = vac_meta["days_metadata"][current_day_key]["notes_list"]

                            edit_mode_key = f"edit_idx_{current_day_key}"
                            if edit_mode_key not in st.session_state:
                                st.session_state[edit_mode_key] = None

                            for idx, note in enumerate(notes_list):
                                c_note, c_edit, c_del = st.columns([0.83, 0.085, 0.085])
                                
                                c_note.markdown(f"<small>• {note.replace(chr(10), '<br>')}</small>", unsafe_allow_html=True)
                                
                                if c_edit.button("✎", key=f"edit_{current_day_key}_{idx}", help="Edit"):
                                    st.session_state[edit_mode_key] = idx
                                    st.session_state[f"edit_text_{current_day_key}"] = note
                                    st.rerun()

                                if c_del.button("×", key=f"del_{current_day_key}_{idx}", help="Delete"):
                                    notes_list.pop(idx)
                                    if st.session_state[edit_mode_key] == idx:
                                        st.session_state[edit_mode_key] = None
                                    save_vacation_meta(vac_meta)
                                    st.rerun()

                            is_editing = st.session_state[edit_mode_key] is not None
                            
                            if is_editing:
                                st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)
                                
                                edit_idx = st.session_state[edit_mode_key]
                                st.markdown(f"<small style='color: #666;'>✏️ Editing note #{edit_idx + 1}</small>", unsafe_allow_html=True)
                                
                                c_input, c_save, c_cancel = st.columns([0.8, 0.1, 0.1])
                                
                                with c_input:
                                    edited_val = st.text_area(
                                        "Edit note", 
                                        value=st.session_state.get(f"edit_text_{current_day_key}", ""), 
                                        key=f"edit_area_{current_day_key}", 
                                        height=20, 
                                        label_visibility="collapsed"
                                    )
                                
                                with c_save:
                                    if st.button("✓", key=f"save_edit_{current_day_key}", help="Save"):
                                        if edited_val.strip():
                                            idx_to_edit = st.session_state[edit_mode_key]
                                            notes_list[idx_to_edit] = edited_val
                                            st.session_state[edit_mode_key] = None
                                            save_vacation_meta(vac_meta)
                                            st.rerun()
                                
                                with c_cancel:
                                    if st.button("✕", key=f"cancel_edit_{current_day_key}", help="Cancel"):
                                        st.session_state[edit_mode_key] = None
                                        st.rerun()
                                    
                            else:
                                new_note = st.chat_input("Add a note...", key=f"chat_{current_day_key}")
                                
                                if new_note:
                                    notes_list.append(new_note)
                                    save_vacation_meta(vac_meta)
                                    st.rerun()

                    # =============== מפה ===============
                    with row2_c2:
                        with st.container(border=True):
                            st.markdown("<div style='font-size: 1.1rem; font-weight: bold; margin-bottom: 8px;'>🗺️ Map & Daily Attractions</div>", unsafe_allow_html=True)
                            
                            schedule = vac_meta.get("schedule", {}).get(str(current_day_key), [])
                            
                            hotels_list = vac_meta.get("hotels", [])
                            active_hotel = None
                            for h in hotels_list:
                                if h["check_in"] <= current_day_key < h["check_out"]:
                                    active_hotel = h
                                    break
                            
                            locations = []
                            for item in schedule:
                                loc = item.get("location") or item.get("coords")
                                if loc and loc.strip():
                                    locations.append(loc.strip())
                            
                            if active_hotel and active_hotel.get('address'):
                                map_location = active_hotel['address']
                            elif locations:
                                map_location = locations[0]
                            else:
                                map_location = vac_meta.get("country")
                            
                            embed_url = f"https://www.google.com/maps?q={map_location.strip().replace(' ', '+')}&output=embed"
                            st.components.v1.iframe(embed_url, height=150, scrolling=False)
                            
                            if locations:
                                if len(locations) == 1:
                                    gmaps_all_link = f"https://www.google.com/maps/search/?api=1&query={locations[0].replace(' ', '+')}"
                                else:
                                    query_string = " OR ".join([f'"{loc}"' for loc in locations])
                                    gmaps_all_link = f"https://www.google.com/maps/search/?api=1&query={query_string.replace(' ', '+')}"

                                st.markdown("""
                                <style>
                                    [data-testid="stLinkButton"] {
                                        margin-top: -17px !important; 
                                    }
                                    [data-testid="stLinkButton"] a {
                                        display: flex !important;
                                        justify-content: center !important;
                                        align-items: center !important;
                                        text-align: center !important;
                                        background-color: #F1F5F9 !important; 
                                        color: #334155 !important;               
                                        border: 1px solid #E2E8F0 !important;   
                                        border-radius: 6px !important;
                                    }
                                    [data-testid="stLinkButton"] a * {
                                        font-size: 0.8rem !important;
                                        color: #334155 !important;                
                                    }
                                    [data-testid="stLinkButton"] a:hover {
                                        background-color: #E2E8F0 !important;   
                                        color: #0F172A !important;
                                    }
                                    [data-testid="stLinkButton"] a:hover * {
                                        color: #0F172A !important;
                                    }
                                </style>
                                """, unsafe_allow_html=True)

                                st.link_button("View all locations for today in Google Maps", gmaps_all_link, use_container_width=True)
                                
                            else:
                                st.info("No locations for today yet.")

                if st.button("➕ Add Attraction", key="fab_attraction", help="Add a new attraction"):
                    add_attraction_dialog(vac_meta, current_nav_date)

        # ------------------------------------------------
        # מודול שכר שעה 
        # ------------------------------------------------

        elif current_project["type"] == "Hourly Wage Tracker":
            st.info("Hourly Wage Tracker module will be built here!")
        
        # ------------------------------------------------
        # מודול חיסכון 
        # ------------------------------------------------

        elif current_project["type"] == "Goal-Based Savings":
            st.info("Goal-Based Savings module will be built here!")
