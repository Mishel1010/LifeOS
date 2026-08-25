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
from datetime import datetime, date, timedelta, time


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
    /* 61. הגדרת סמן יד לכל המרכיבים של תיבת התאריך */
    div[data-testid="stDateInput"] > div,
    div[data-testid="stDateInput"] input,
    div[role="dialog"] div[data-testid="stDateInput"] > div,
    div[role="dialog"] div[data-testid="stDateInput"] input {
        cursor: pointer !important;
        transition: all 0.2s ease-in-out !important;
        border-radius: 8px !important;
    }
    /* 62. אפקט ריחוף */
    div[data-testid="stDateInput"]:hover > div > div,
    div[role="dialog"] div[data-testid="stDateInput"]:hover > div > div {
        border-color: #1976d2 !important;
        box-shadow: 0 0 8px rgba(25, 118, 210, 0.25) !important;
    }
    /* 63. אפקט הגדלה בעת ריחוף מעל סמלי המפה והעריכה */
    .hover-scale {
        display: inline-block;
        transition: transform 0.2s ease-in-out;
    }
    .hover-scale:hover {
        transform: scale(1.25);
    }
    .flight-card {
        padding: 10px;
        border-radius: 8px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: all 0.2s ease-in-out;
        background-color: var(--secondary-background-color);
    }
    .flight-card:hover {
        background-color: rgba(128, 128, 128, 0.1);
        transform: scale(1.01);
        border-color: #1976d2;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

#------------------------------------------------------
# פונקציות וקטעי קוד שאני צריך שיהיו בתחילת הקוד 
#------------------------------------------------------

MONTH_TO_NUM = {
    "January": 1, "February": 2, "March": 3, "April": 4, 
    "May": 5, "June": 6, "July": 7, "August": 8, 
    "September": 9, "October": 10, "November": 11, "December": 12
}
NUM_TO_MONTH = {v: k for k, v in MONTH_TO_NUM.items()}

months = list(MONTH_TO_NUM.keys())
current_year = datetime.now().year
years = list(range(2025, current_year + 50))

if "select_month_box" not in st.session_state:
    st.session_state.select_month_box = months[datetime.now().month - 1]

if "select_year_box" not in st.session_state:
    st.session_state.select_year_box = current_year if current_year in years else years[0]

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
    "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal",
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
    "Oman": "🇴🇲", "Pakistan": "🇵🇰", "Palau": "🇵🇼", "Panama": "🇵🇦", 
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
    
def format_duration(hours_float):
    try:
        total_minutes = int(round(float(hours_float) * 60))
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours == 0 and minutes == 0:
            return "0 min"
        elif minutes == 0:
            return f"{hours} hrs"
        elif hours == 0:
            return f"{minutes} mins"
        else:
            return f"{hours} hrs<br>{minutes:02d} mins"
    except:
        return "1 hour"

minute_options = [f"{i:02d}" for i in range(60)]
hour_options = [f"{i:02d}" for i in range(24)]

#------------------------------------------------------
# אתחול מערכת ההזדהות
#------------------------------------------------------
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

# ============== בדיקת סטטוס ההתחברות ======================
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
            shutil.rmtree(project_folder) 
            
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

        item_name = st.text_input("Description (e.g., Groceries, Salary) - OPTIONAL", max_chars=25)
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
            if amount is not None and amount > 0:
                chosen_day = int(selected_date.day)
                chosen_month_str = NUM_TO_MONTH[selected_date.month]
                chosen_year = int(selected_date.year)

                final_item_name = item_name.strip() if item_name and item_name.strip() else "..."
                
                new_row = pd.DataFrame([{
                    "day": chosen_day,
                    "Description": final_item_name,
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
                st.error("Please enter a valid amount.")

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
            new_name = st.text_input("Description / Name", value=curr_name, max_chars=25)
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
        st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)

        current_start = datetime.strptime(vac_meta.get("start_date", str(date.today())), "%Y-%m-%d").date()
        current_end = datetime.strptime(vac_meta.get("end_date", str(date.today())), "%Y-%m-%d").date()
        current_travelers = int(vac_meta.get("travelers", 2))
        current_budget = float(vac_meta.get("budget", 10000.0))
        
        selected_countries = vac_meta.get("countries", [])
        if not selected_countries and "country" in vac_meta and vac_meta["country"] != "Select Country...":
            selected_countries = [vac_meta["country"]]

        updated_segments = []

        with st.form("edit_trip_form"):
            st.markdown("Update your trip logistics and dates:")
            
            if len(selected_countries) == 1:
                trip_dates = st.date_input("🗓️ Trip Dates (Start & End)", value=(current_start, current_end))
            else:
                st.markdown("##### Trip Segments:")
                
                existing_segments = vac_meta.get("segments", [{"start": str(current_start), "end": str(current_end), "country": selected_countries[0]}])
                
                if f"edit_num_segments_{current_project['id']}" not in st.session_state:
                    st.session_state[f"edit_num_segments_{current_project['id']}"] = len(existing_segments)
                
                num_segs = st.session_state[f"edit_num_segments_{current_project['id']}"]
                
                for s in range(num_segs):
                    default_seg = existing_segments[s] if s < len(existing_segments) else existing_segments[-1]
                    s_def_start = datetime.strptime(default_seg["start"], "%Y-%m-%d").date()
                    s_def_end = datetime.strptime(default_seg["end"], "%Y-%m-%d").date()
                    s_def_c = default_seg["country"]
                    if s_def_c not in selected_countries:
                        s_def_c = selected_countries[0]
                    c_idx = selected_countries.index(s_def_c)

                    st.markdown(f"**Segment {s+1}**")
                    s_col1, s_col2 = st.columns([2, 1])
                    with s_col1:
                        seg_dates = st.date_input(f"Dates (Segment {s+1})", value=(s_def_start, s_def_end), key=f"edit_seg_dates_{s}")
                    with s_col2:
                        s_country = st.selectbox(f"Country", options=selected_countries, index=c_idx, key=f"edit_seg_country_{s}")
                    
                    updated_segments.append({"dates": seg_dates, "country": s_country})

                if st.form_submit_button("➕ Add Another Segment"):
                    st.session_state[f"edit_num_segments_{current_project['id']}"] += 1
                    st.rerun()

            t_col1, t_col2 = st.columns(2)
            with t_col1:
                new_travelers = st.number_input("Number of Travelers", min_value=1, value=current_travelers, step=1)
            with t_col2:
                new_budget = st.number_input("Total Budget (ILS)", min_value=0.0, value=current_budget, step=500.0)

            if st.form_submit_button("Save Changes 💾", use_container_width=True, type="primary"):
                if len(selected_countries) == 1:
                    if len(trip_dates) < 2:
                        st.error("Please select BOTH a start and end date.")
                        st.stop()
                    new_start, new_end = trip_dates[0], trip_dates[1]
                    vac_meta["segments"] = [{"start": str(new_start), "end": str(new_end), "country": selected_countries[0]}]
                else:
                    if not updated_segments:
                        st.error("Please define at least one segment.")
                        st.stop()
                    
                    final_segments = []
                    all_starts, all_ends = [], []
                    for seg in updated_segments:
                        if len(seg["dates"]) < 2:
                            st.error("Please select BOTH a start and end date for all segments.")
                            st.stop()
                        s_st, s_en = seg["dates"][0], seg["dates"][1]
                        final_segments.append({"start": str(s_st), "end": str(s_en), "country": seg["country"]})
                        all_starts.append(s_st)
                        all_ends.append(s_en)
                        
                    new_start = min(all_starts)
                    new_end = max(all_ends)
                    vac_meta["segments"] = final_segments

                if new_start > new_end:
                    st.error("Start date cannot be after end date.")
                else:
                    vac_meta["start_date"] = str(new_start)
                    vac_meta["end_date"] = str(new_end)
                    vac_meta["travelers"] = new_travelers
                    vac_meta["budget"] = new_budget
                    
                    if "days_metadata" not in vac_meta:
                        vac_meta["days_metadata"] = {}

                    def init_or_update_day(d_str, country_name):
                        if d_str not in vac_meta["days_metadata"]:
                            vac_meta["days_metadata"][d_str] = {
                                "country": country_name,
                                "notes_list": [],
                                "schedule": []
                            }
                        else:
                            vac_meta["days_metadata"][d_str]["country"] = country_name
                            if "notes_list" not in vac_meta["days_metadata"][d_str]:
                                vac_meta["days_metadata"][d_str]["notes_list"] = []
                            if "schedule" not in vac_meta["days_metadata"][d_str]:
                                vac_meta["days_metadata"][d_str]["schedule"] = []

                    if len(selected_countries) == 1:
                        single_c = selected_countries[0]
                        curr = new_start
                        while curr <= new_end:
                            init_or_update_day(str(curr), single_c)
                            curr += dt.timedelta(days=1)
                    else:
                        for seg in vac_meta["segments"]:
                            s_dt = datetime.strptime(seg["start"], "%Y-%m-%d").date()
                            e_dt = datetime.strptime(seg["end"], "%Y-%m-%d").date()
                            c_name = seg["country"]
                            
                            curr = s_dt
                            while curr <= e_dt:
                                init_or_update_day(str(curr), c_name)
                                curr += dt.timedelta(days=1)

                    vac_meta["days_metadata"] = dict(sorted(vac_meta["days_metadata"].items()))

                    curr_nav = datetime.strptime(vac_meta.get("current_trip_date", str(new_start)), "%Y-%m-%d").date()
                    if curr_nav < new_start or curr_nav > new_end:
                        vac_meta["current_trip_date"] = str(new_start)

                    save_vacation_meta(vac_meta)
                    st.rerun()

        st.markdown("#### 📂 Trip Documents Manager")
        render_document_manager(f"{project_folder}/documents", can_edit=True, show_download=False)

    @st.dialog("✏️ Edit Attraction")
    def edit_attraction_dialog(v_meta, day_key, idx, item):
        with st.container(border=True):
            st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)        
            day_str = str(day_key)
            
            try:
                def_res_date = datetime.strptime(item.get('date', day_str), "%Y-%m-%d").date()
            except:
                def_res_date = current_nav_date

            state_key_needs = f"edit_att_needs_{day_str}_{idx}"
            state_key_booked = f"edit_att_booked_{day_str}_{idx}"
            
            if state_key_needs not in st.session_state:
                st.session_state[state_key_needs] = item.get('needs_booking', False)
            if state_key_booked not in st.session_state:
                st.session_state[state_key_booked] = item.get('booked', False)

            needs_booking = st.checkbox(
                "🎟️ Needs to be booked in advance?", 
                value=st.session_state[state_key_needs],
                key=f"chk_att_needs_{day_str}_{idx}",
                on_change=lambda: st.session_state.update({state_key_needs: st.session_state[f"chk_att_needs_{day_str}_{idx}"]})
            )

            is_booked = False
            if needs_booking:
                is_booked = st.checkbox(
                    "✅ Already Booked / Reserved?", 
                    value=st.session_state[state_key_booked],
                    key=f"chk_att_booked_{day_str}_{idx}",
                    on_change=lambda: st.session_state.update({state_key_booked: st.session_state[f"chk_att_booked_{day_str}_{idx}"]})
                )

            new_name = st.text_input("Description", value=item.get('name', ''), key=f"att_name_{day_str}_{idx}")

            try:
                t_start = datetime.strptime(v_meta.get("start_date", str(date.today())), "%Y-%m-%d").date()
                t_end = datetime.strptime(v_meta.get("end_date", str(date.today() + timedelta(days=7))), "%Y-%m-%d").date()
            except:
                t_start, t_end = date.today(), date.today() + timedelta(days=7)
            
            try:
                def_time = datetime.strptime(item.get('time', '10:00:00'), "%H:%M:%S").time()
            except:
                def_time = datetime.strptime("10:00:00", "%H:%M:%S").time()

            col_d, col_h, com_m = st.columns([1, 0.5, 0.5], vertical_alignment="center")
            with col_d:
                reservation_date = st.date_input("Date", value=def_res_date, format="DD/MM/YYYY", key=f"edit_att_date_{day_str}_{idx}")
            with col_h:
                curr_hr_str = f"{def_time.hour:02d}"
                hr_idx = hour_options.index(curr_hr_str) if curr_hr_str in hour_options else 0
                reservation_hour = st.selectbox("Hour", options=hour_options, index=hr_idx, key=f"edit_att_hr_{day_str}_{idx}")
            with com_m:
                curr_min_str = f"{def_time.minute:02d}"
                min_idx = minute_options.index(curr_min_str) if curr_min_str in minute_options else 0
                reservation_minute = st.selectbox("Minute", options=minute_options, index=min_idx, key=f"edit_att_min_{day_str}_{idx}")

            start_time = time(int(reservation_hour), int(reservation_minute))
            
            curr_dur_val = float(item.get('duration', 2.0))
            def_hrs = int(curr_dur_val)
            def_mins = int(round((curr_dur_val - def_hrs) * 60))

            col_lbl, col_hr, col_min = st.columns([0.4, 1, 1], vertical_alignment="center")
            with col_lbl:
                st.markdown("<div style='margin-top: 10px; font-size: 0.85rem; font-weight: 400;'>Duration:</div>", unsafe_allow_html=True)  
                
            dur_hours = col_hr.number_input("hours", min_value=0, max_value=24, value=def_hrs, step=1, key=f"att_hrs_{day_str}_{idx}")
            
            def_mins_str = f"{def_mins:02d}" if def_mins in range(60) else "00"
            dur_min_idx = minute_options.index(def_mins_str) if def_mins_str in minute_options else 0
            dur_mins = col_min.selectbox("minutes", options=minute_options, index=dur_min_idx, key=f"att_mins_{day_str}_{idx}")
            
            duration_hours = int(dur_hours) + (int(dur_mins) / 60.0)
            
            new_coords_str = st.text_input("📍 Location", value=item.get('coords', ''), key=f"att_coords_{day_str}_{idx}")
            
            att_budget = float(item.get('budget', 0.0))
            if (needs_booking and is_booked):
                att_budget = st.number_input("💰 Budget (₪)", min_value=0.0, value=att_budget, step=50.0, key=f"att_budget_{day_str}_{idx}")
            else:
                att_budget = 0.0

            new_notes = st.text_area("📝 Notes", value=item.get('notes', ''), key=f"att_notes_{day_str}_{idx}")
            
            st.write("")
            col_save, col_del = st.columns(2)
            
            with col_save:
                save_clicked = st.button("Save Changes", use_container_width=True, type="primary", key=f"att_save_{day_str}_{idx}")
            with col_del:
                delete_clicked = st.button("Delete", use_container_width=True, key=f"att_del_{day_str}_{idx}")
            
            if save_clicked:
                if not new_name.strip():
                    st.error("Please enter a description.")
                elif not (t_start <= reservation_date <= t_end):
                    st.error(f"❌ Error: Date must be within trip bounds ({t_start.strftime('%d/%m/%Y')} - {t_end.strftime('%d/%m/%Y')})")
                else:
                    target_day_str = str(reservation_date)
                    updated_item = {
                        "name": new_name.strip(),
                        "date": target_day_str,
                        "time": str(start_time),
                        "duration": duration_hours,
                        "coords": new_coords_str.strip(),
                        "budget": att_budget if (needs_booking and is_booked) else 0.0,
                        "needs_booking": needs_booking,
                        "booked": is_booked if needs_booking else False,
                        "notes": new_notes.strip(),
                        "type": "attraction"
                    }

                    if "days_metadata" not in v_meta: v_meta["days_metadata"] = {}

                    if target_day_str != day_str:
                        if day_str in v_meta["days_metadata"] and "schedule" in v_meta["days_metadata"][day_str]:
                            if idx < len(v_meta["days_metadata"][day_str]["schedule"]):
                                v_meta["days_metadata"][day_str]["schedule"].pop(idx)
                        
                        if target_day_str not in v_meta["days_metadata"]: 
                            v_meta["days_metadata"][target_day_str] = {"notes_list": [], "schedule": []}
                        if "schedule" not in v_meta["days_metadata"][target_day_str]: 
                            v_meta["days_metadata"][target_day_str]["schedule"] = []
                            
                        v_meta["days_metadata"][target_day_str]["schedule"].append(updated_item)
                    else:
                        if day_str not in v_meta["days_metadata"]: v_meta["days_metadata"][day_str] = {"notes_list": [], "schedule": []}
                        if "schedule" not in v_meta["days_metadata"][day_str]: v_meta["days_metadata"][day_str]["schedule"] = []
                        v_meta["days_metadata"][day_str]["schedule"][idx] = updated_item

                    save_vacation_meta(v_meta)
                    
                    if state_key_needs in st.session_state: del st.session_state[state_key_needs]
                    if state_key_booked in st.session_state: del st.session_state[state_key_booked]
                    
                    st.success("Updated successfully!")
                    st.rerun()
                    
            if delete_clicked:
                if day_str in v_meta.get("days_metadata", {}):
                    if "schedule" in v_meta["days_metadata"][day_str]:
                        v_meta["days_metadata"][day_str]["schedule"].pop(idx)
                        save_vacation_meta(v_meta)
                        
                        if state_key_needs in st.session_state: del st.session_state[state_key_needs]
                        if state_key_booked in st.session_state: del st.session_state[state_key_booked]
                        
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
                
            default_price = float(active_hotel.get("price", 0.0)) if active_hotel else 0.0
            default_notes = active_hotel.get("notes", "") if active_hotel else ""

            hotel_name = st.text_input("Hotel Name", value=default_name)
            hotel_address = st.text_input("📍 Address / Location", value=default_address)
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                check_in = st.date_input("Check-in Date", value=default_checkin)
            with col_d2:
                check_out = st.date_input("Check-out Date", value=default_checkout)
                
            hotel_price = st.number_input("💰 Total Hotel Cost (₪)", min_value=0.0, value=default_price, step=100.0)
            hotel_notes = st.text_area("📝 Hotel Notes (Booking ref, breakfast, etc.)", value=default_notes)
            
            st.write("")
            
            col_save, col_del = st.columns(2)
            save_clicked = col_save.form_submit_button("Save Hotel Details", use_container_width=True, type="primary")
            delete_clicked = col_del.form_submit_button("Delete Hotel", use_container_width=True)
            
            if save_clicked:
                if "hotels" not in v_meta: 
                    v_meta["hotels"] = []
                
                new_hotel_data = {
                    "name": hotel_name,
                    "address": hotel_address,
                    "check_in": str(check_in),
                    "check_out": str(check_out),
                    "price": hotel_price,
                    "notes": hotel_notes
                }
                
                if active_hotel in v_meta["hotels"]:
                    v_meta["hotels"].remove(active_hotel)
                v_meta["hotels"].append(new_hotel_data)
                
                save_vacation_meta(v_meta)
                st.success("Hotel saved successfully!")
                st.rerun()
                
            if delete_clicked:
                if "hotels" in v_meta:
                    if active_hotel in v_meta["hotels"]:
                        v_meta["hotels"].remove(active_hotel)
                        save_vacation_meta(v_meta)
                        st.success("Hotel deleted successfully!")
                        st.rerun()
                    else:
                        st.warning("Hotel not found in records.")

    def render_document_manager(docs_folder, can_edit=False, show_download=True):
        os.makedirs(docs_folder, exist_ok=True)
        
        if can_edit:
            uploaded_files = st.file_uploader("Upload flight tickets, insurance, etc.", accept_multiple_files=True, key=f"uploader_{docs_folder}")
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    with open(os.path.join(docs_folder, uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                st.rerun()

        existing_docs = os.listdir(docs_folder) if os.path.exists(docs_folder) else []
        if not existing_docs:
            st.info("No documents uploaded yet.")
        else:
            for doc in existing_docs:
                file_path = os.path.join(docs_folder, doc)
                
                col_name, col_actions = st.columns([0.7, 0.3], vertical_alignment="center")

                with col_name:
                    st.markdown(f"📄 <b>{doc}</b>", unsafe_allow_html=True)

                with col_actions:
                    if show_download:
                        with open(file_path, "rb") as f:
                            file_bytes = f.read()
                        sub_cols = st.columns(2 if can_edit else 1, vertical_alignment="center")
                        with sub_cols[0]:
                            st.download_button("Download", file_bytes, doc, key=f"dl_{docs_folder}_{doc}", help="Download", use_container_width=True)
                        if can_edit:
                            with sub_cols[1]:
                                if st.button("🗑️", key=f"del_{docs_folder}_{doc}", help="Delete", use_container_width=True):
                                    os.remove(file_path)
                                    st.rerun()
                    else:
                        if can_edit:
                            if st.button("Delete", key=f"del_only_{docs_folder}_{doc}", use_container_width=True):
                                os.remove(file_path)
                                st.rerun()

    @st.dialog("Trip Options")
    def trip_menu_dialog(vac_meta, project_folder):
        st.markdown("Choose what you would like to view or edit:")
        st.write("")
            
        if st.button("Trip Overview & Documents", use_container_width=True):
            st.session_state["open_dialog"] = "overview"
            st.rerun()
            
        if st.button("Trip Expenses Tracker", use_container_width=True):
            st.session_state["open_dialog"] = "expenses"
            st.rerun()

        if st.button("Manage Flights", use_container_width=True):
            st.session_state["open_dialog"] = "flights"
            st.rerun()

        if st.button("⚙️ Edit Trip Settings", use_container_width=True, type="primary"):
            st.session_state["open_dialog"] = "edit_settings"
            st.rerun()

    @st.dialog("Trip Overview & Documents")
    def trip_overview_dialog(vac_meta, project_folder):
        st.markdown("<h2 style='text-align: center;'>Trip Overview</h2>", unsafe_allow_html=True)
        
        today = date.today()
        try:
            start_d = datetime.strptime(vac_meta.get("start_date", str(today)), "%Y-%m-%d").date()
            end_d = datetime.strptime(vac_meta.get("end_date", str(today)), "%Y-%m-%d").date()
        except:
            start_d, end_d = today, today + timedelta(days=1)
            
        total_trip_days = (end_d - start_d).days + 1
        
        if today < start_d:
            days_to_go = (start_d - today).days
            st.markdown(f"<h3 style='text-align: center; color: #1976d2;'>⏳ {days_to_go} Days To Go! 🚀</h3>", unsafe_allow_html=True)
        elif start_d <= today <= end_d:
            current_day_num = (today - start_d).days + 1
            progress_val = current_day_num / total_trip_days
            st.markdown(f"<h3 style='text-align: center; color: #2e7d32;'>🌴 Day {current_day_num} of {total_trip_days} ✈️</h3>", unsafe_allow_html=True)
            st.progress(progress_val)
        else:
            st.markdown(f"<h3 style='text-align: center; color: #6c757d;'>🏁 Trip Completed</h3>", unsafe_allow_html=True)
            
        st.divider()
        
        total_budget = float(vac_meta.get("budget", 0))
        
        category_expenses = {
            "Attractions": 0.0,
            "Restaurants": 0.0,
            "Transportation": 0.0,
            "Accommodation": 0.0,
            "Shopping": 0.0,
            "Flights": 0.0,
            "Other": 0.0
        }
        
        hotels_expenses = sum(float(h.get("price", 0.0)) for h in vac_meta.get("hotels", []))
        category_expenses["Accommodation"] += hotels_expenses

        flights_list = vac_meta.get("flights", [])
        flights_expenses = sum(float(f.get("price", 0.0)) for f in flights_list)
        category_expenses["Flights"] += flights_expenses
        
        for d_key, d_val in vac_meta.get("days_metadata", {}).items():
            for item in d_val.get("schedule", []):
                cost = float(item.get("budget", 0.0))
                if cost > 0:
                    i_type = item.get("type", "attraction")
                    if i_type == "attraction":
                        category_expenses["Attractions"] += cost
                    elif i_type == "transit":
                        category_expenses["Transportation"] += cost
                    elif i_type == "restaurant":
                        category_expenses["Restaurants"] += cost
                
        trip_expenses_file = f"{project_folder}/trip_expenses.csv"
        if os.path.exists(trip_expenses_file):
            df_exp = pd.read_csv(trip_expenses_file)
            if not df_exp.empty and "Amount" in df_exp.columns and "Expense Type" in df_exp.columns:
                for _, row in df_exp.iterrows():
                    amt = float(row["Amount"])
                    e_type = str(row["Expense Type"]).strip()
                    
                    if e_type == "Shopping":
                        category_expenses["Shopping"] += amt
                    elif e_type == "Restaurants":
                        category_expenses["Restaurants"] += amt
                    elif e_type == "Transportation":
                        category_expenses["Transportation"] += amt
                    elif e_type == "Attractions":
                        category_expenses["Attractions"] += amt
                    else:
                        category_expenses["Other"] += amt

        total_expenses = sum(category_expenses.values())
        balance = total_budget - total_expenses
        bal_sign = "+" if balance >= 0 else ""
        
        with st.container(border=True):
            col_b1, col_b2 = st.columns(2)
            col_b1.markdown(f"**Budget:**")
            col_b2.markdown(f"₪{total_budget:,.2f}")
            
            col_b1, col_b2 = st.columns(2)
            col_b1.markdown(f"**Total Expenses:**")
            col_b2.markdown(f"₪{total_expenses:,.2f}")
            
            col_b1, col_b2 = st.columns(2)
            col_b1.markdown(f"**Balance:**")
            col_b2.markdown(f"<span style='color: {'#2e7d32' if balance >=0 else '#c62828'};'><b>{bal_sign}₪{balance:,.2f}</b></span>", unsafe_allow_html=True)

        st.divider()
        st.markdown("#### 📊 Expenses Breakdown")
        
        active_categories = {k: v for k, v in category_expenses.items() if v > 0}
        
        if not active_categories:
            st.info("No expenses recorded yet to display the chart.")
        else:
            import plotly.express as px
            
            df_pie = pd.DataFrame({
                "Category": list(active_categories.keys()),
                "Amount": list(active_categories.values())
            })
            
            fig = px.pie(
                df_pie, 
                names="Category", 
                values="Amount", 
                hole=0.4, 
                color_discrete_sequence=['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#FF6D01']
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=13)
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=350,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.markdown("#### 📁 Relevant Documents")
        render_document_manager(f"{project_folder}/documents", can_edit=False, show_download=True)

    @st.dialog("Trip Expenses Tracker")
    def trip_expenses_dialog(project_folder, vac_meta):
        st.markdown("""
            <style>
                div[role="dialog"] {
                    width: 80% !important;
                    max-width: 900px !important;
                }
                .tx-line {
                    display: flex;
                    align-items: center;
                    padding: 12px 12px !important;
                    margin-bottom: 14px;
                    border-radius: 6px;
                    transition: background-color 0.2s ease;
                    width: 100%;
                    box-sizing: border-box !important;
                }
                .tx-line:hover {
                    background-color: rgba(128, 128, 128, 0.18) !important;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center;'>Expenses Tracker</h2>", unsafe_allow_html=True)
        st.write("")
        
        expenses_file = f"{project_folder}/trip_expenses.csv"
        
        def delete_expense_callback(exp_id):
            if os.path.exists(expenses_file):
                temp_df = pd.read_csv(expenses_file)
                temp_df = temp_df[temp_df["ID"] != exp_id]
                temp_df.to_csv(expenses_file, index=False)

        if os.path.exists(expenses_file):
            df_exp = pd.read_csv(expenses_file)
        else:
            df_exp = pd.DataFrame(columns=["ID", "Date", "Expense Type", "Description", "Amount"])
            
        if "ID" not in df_exp.columns or df_exp["ID"].isna().any():
            df_exp["ID"] = range(len(df_exp))
            df_exp.to_csv(expenses_file, index=False)

        if f"edit_trip_exp_id_{project_folder}" not in st.session_state:
            st.session_state[f"edit_trip_exp_id_{project_folder}"] = None

        editing_id = st.session_state[f"edit_trip_exp_id_{project_folder}"]

        if editing_id is not None:
            row_match = df_exp[df_exp["ID"] == editing_id]
            if not row_match.empty:
                current_row = row_match.iloc[0]
                st.markdown("---")
                st.markdown(f"##### ✏️ Edit Expense (ID: {editing_id})")
                
                with st.form(f"edit_inline_exp_form_{editing_id}"):
                    try:
                        def_date = datetime.strptime(str(current_row["Date"]), "%Y-%m-%d").date()
                    except:
                        def_date = date.today()

                    new_date = st.date_input("Date", value=def_date, format="DD/MM/YYYY")
                    
                    exp_types = ["Shopping", "Restaurants", "Transportation", "Accommodation", "Other"]
                    curr_type = str(current_row["Expense Type"])
                    t_idx = exp_types.index(curr_type) if curr_type in exp_types else 0
                    new_type = st.selectbox("Expense Type", exp_types, index=t_idx)
                    
                    new_desc = st.text_input("Description", value=str(current_row["Description"]), max_chars=25)
                    new_amt = st.number_input("Amount (ILS)", value=float(current_row["Amount"]), min_value=0.0, step=10.0)
                    
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.form_submit_button("Save Changes", use_container_width=True, type="primary"):
                            if new_amt > 0:
                                mask = df_exp["ID"] == editing_id
                                df_exp.loc[mask, "Date"] = str(new_date)
                                df_exp.loc[mask, "Expense Type"] = new_type
                                df_exp.loc[mask, "Description"] = new_desc.strip()[:25] if new_desc else "..."
                                df_exp.loc[mask, "Amount"] = new_amt
                                df_exp.to_csv(expenses_file, index=False)
                                st.session_state[f"edit_trip_exp_id_{project_folder}"] = None
                                st.success("Expense updated successfully!")
                                st.rerun()
                            else:
                                st.error("Please enter a valid amount.")
                    with col_cancel:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            st.session_state[f"edit_trip_exp_id_{project_folder}"] = None
                            st.rerun()
                st.markdown("---")

        if df_exp.empty:
            st.info("No expenses recorded yet. You can add expenses using the 'Add' button on the main screen.")
        else:
            hc_main, hc_edit_space = st.columns([0.96, 0.04])
            with hc_main:
                st.markdown("""
                    <div style='display: flex; align-items: center; width: 100%; padding: 4px 12px; margin-bottom: 8px;'>
                        <div style='flex: 0.13; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>DATE</div>
                        <div style='flex: 0.25; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>TYPE</div>
                        <div style='flex: 0.44; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>DESCRIPTION</div>
                        <div style='flex: 0.18; text-align: center; color: var(--text-color, #adb5bd); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;'>AMOUNT</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 0px 0px 4px 0px; border-color: rgba(128, 128, 128, 0.2);'>", unsafe_allow_html=True)

            for idx, row in df_exp.iterrows():
                e_id = int(row["ID"]) if pd.notna(row["ID"]) else idx
                r_date = str(row["Date"])
                r_type = str(row["Expense Type"])
                r_desc = str(row["Description"])
                r_amt = float(row["Amount"]) if pd.notna(row["Amount"]) else 0.0

                t_row, p_row = st.columns([0.96, 0.04], vertical_alignment="center")
                
                with t_row:
                    st.markdown(f"""
                        <div class='tx-line'>
                            <div style='flex: 0.13; text-align: center; font-size: 0.9rem; font-weight: 500; opacity: 0.85;'>{r_date}</div>
                            <div style='flex: 0.25; text-align: center;'><span style='font-size: 0.8rem; opacity: 0.8; background: rgba(25, 118, 210, 0.15); padding: 3px 10px; border-radius: 12px; font-weight: 500;'>{r_type}</span></div>
                            <div style='flex: 0.44; text-align: center; font-size: 0.95rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 0 5px;'>{r_desc}</div>
                            <div style='flex: 0.18; text-align: center; font-size: 0.95rem; font-weight: 700; color: #c62828;'>₪{r_amt:,.2f}-</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with p_row:
                    st.button("🗑️", key=f"del_exp_{e_id}", help="Delete expense", on_click=delete_expense_callback, args=(e_id,))
                        
                st.markdown("<div style='border-bottom: 1px solid rgba(128, 128, 128, 0.1); margin: 0px 0;'></div>", unsafe_allow_html=True)

    @st.dialog("➕ Add to Itinerary / Expenses")
    def unified_trip_add_dialog(v_meta, day_key, project_folder):
        try:
            t_start = datetime.strptime(v_meta.get("start_date", str(date.today())), "%Y-%m-%d").date()
            t_end = datetime.strptime(v_meta.get("end_date", str(date.today() + timedelta(days=7))), "%Y-%m-%d").date()
        except:
            t_start, t_end = date.today(), date.today() + timedelta(days=7)

        if "add_modal_choice" not in st.session_state:
            st.session_state.add_modal_choice = None

        add_choice = st.selectbox(
            "What would you like to add?",
            ["Activity", "Transit between locations", "Restaurant", "Trip Expense (Shopping, Restaurant, etc.)"],
            index=None,
            placeholder="Select option to add...",
            key="add_modal_choice"
        )

        # אופציה 1: הוספת אטרקציה
        if add_choice == "Activity":
            with st.container(border=True):
                st.markdown("##### 🎯 Attraction Details")
                
                add_att_needs_key = "add_att_needs_booking"
                add_att_booked_key = "add_att_is_booked"
                
                if add_att_needs_key not in st.session_state:
                    st.session_state[add_att_needs_key] = False
                if add_att_booked_key not in st.session_state:
                    st.session_state[add_att_booked_key] = False

                needs_booking = st.checkbox(
                    "🎟️ Needs to be booked in advance?", 
                    value=st.session_state[add_att_needs_key],
                    key="chk_add_att_needs",
                    on_change=lambda: st.session_state.update({add_att_needs_key: st.session_state["chk_add_att_needs"]})
                )

                is_booked = False
                if needs_booking:
                    is_booked = st.checkbox(
                        "✅ Already Booked / Reserved?", 
                        value=st.session_state[add_att_booked_key],
                        key="chk_add_att_booked",
                        on_change=lambda: st.session_state.update({add_att_booked_key: st.session_state["chk_add_att_booked"]})
                    )

                new_name = st.text_input("Description", key="add_att_name")
                
                col_d, col_h, col_m = st.columns([1, 0.5, 0.5], vertical_alignment="center")
                with col_d:
                    att_date = st.date_input("Date", value=current_nav_date, format="DD/MM/YYYY", key="add_att_date")
                with col_h:
                    att_hour = st.selectbox("Hour", options=hour_options, index=10, key="add_att_hour")
                with col_m:
                    att_minute = st.selectbox("Minute", options=minute_options, index=0, key="add_att_min")
                
                start_time = time(int(att_hour), int(att_minute))

                col_lbl, col_hr, col_min = st.columns([0.4, 1, 1], vertical_alignment="center")
                with col_lbl:
                    st.markdown("<div style='margin-top: 10px; font-size: 0.85rem; font-weight: 400;'>Duration:</div>", unsafe_allow_html=True)  
                
                dur_hours = col_hr.number_input("hours", min_value=0, max_value=24, value=2, step=1, key="add_att_dur_hrs")
                dur_mins = col_min.selectbox("minutes", options=minute_options, index=0, key="add_att_dur_mins")
                
                duration_hours = int(dur_hours) + (int(dur_mins) / 60.0)
                
                new_coords_str = st.text_input("📍 Location", key="add_att_coords")
                
                att_budget = 0.0
                if (needs_booking and is_booked):
                    att_budget = st.number_input("💰 Budget (₪)", min_value=0.0, value=0.0, step=50.0, key="add_att_budget")
                
                new_notes = st.text_area("📝 Notes", key="add_att_notes")
                
                st.write("")
                if st.button("Add Attraction", use_container_width=True, type="primary", key="add_att_submit"):
                    if not new_name.strip():
                        st.error("Please enter a description.")
                    elif start_time is None:
                        st.error("Please select a start time.")
                    elif not (t_start <= att_date <= t_end):
                        st.error(f"Error: Date must be within trip bounds ({t_start.strftime('%d/%m/%Y')} - {t_end.strftime('%d/%m/%Y')})")
                    else:
                        new_item = {
                            "name": new_name.strip(),
                            "date": str(att_date),
                            "time": str(start_time),
                            "duration": duration_hours,
                            "coords": new_coords_str.strip(), 
                            "budget": att_budget if (not needs_booking or (needs_booking and is_booked)) else 0.0,
                            "needs_booking": needs_booking,
                            "booked": is_booked if needs_booking else False,
                            "notes": new_notes.strip(),
                            "type": "attraction"
                        }
                        
                        day_str = str(day_key)
                        if "days_metadata" not in v_meta: v_meta["days_metadata"] = {}
                        if day_str not in v_meta["days_metadata"]: v_meta["days_metadata"][day_str] = {"notes_list": [], "schedule": []}
                        if "schedule" not in v_meta["days_metadata"][day_str]: v_meta["days_metadata"][day_str]["schedule"] = []
                        
                        v_meta["days_metadata"][day_str]["schedule"].append(new_item)
                        save_vacation_meta(v_meta)
                        
                        if add_att_needs_key in st.session_state: del st.session_state[add_att_needs_key]
                        if add_att_booked_key in st.session_state: del st.session_state[add_att_booked_key]
                        
                        st.success("Attraction added successfully!")
                        st.rerun()

        # אופציה 2: הוספת נסיעה 
        elif add_choice == "Transit between locations":
            with st.container(border=True):
                st.markdown("##### 🚗 Transit Details")
                
                add_needs_key = "add_transit_needs_booking"
                add_booked_key = "add_transit_is_booked"
                
                if add_needs_key not in st.session_state:
                    st.session_state[add_needs_key] = False
                if add_booked_key not in st.session_state:
                    st.session_state[add_booked_key] = False

                needs_booking = st.checkbox(
                    "🎟️ Needs to be booked in advance?", 
                    value=st.session_state[add_needs_key],
                    key="chk_add_needs_booking",
                    on_change=lambda: st.session_state.update({add_needs_key: st.session_state["chk_add_needs_booking"]})
                )

                is_booked = False
                if needs_booking:
                    is_booked = st.checkbox(
                        "✅ Already Booked / Reserved?", 
                        value=st.session_state[add_booked_key],
                        key="chk_add_is_booked",
                        on_change=lambda: st.session_state.update({add_booked_key: st.session_state["chk_add_is_booked"]})
                    )

                col_d, col_h, com_m = st.columns([1, 0.5, 0.5], vertical_alignment="center")
                with col_d:
                    transit_date = st.date_input("Transit Date", value=current_nav_date, format="DD/MM/YYYY", key="add_t_date")
                with col_h:
                    transit_hour = st.selectbox("Hour", options=hour_options, index=10, key="add_t_hour")
                with com_m:
                    transit_minute = st.selectbox("Minute", options=minute_options, index=0, key="add_t_min")

                transit_time = time(int(transit_hour), int(transit_minute))

                col_lbl, col_hr, col_min = st.columns([0.4, 1, 1], vertical_alignment="center")
                with col_lbl:
                    st.markdown("<div style='margin-top: 10px; font-size: 0.85rem; font-weight: 400;'>Duration:</div>", unsafe_allow_html=True)  
                
                dur_hours = col_hr.number_input("hours", min_value=0, max_value=24, value=1, step=1, key="add_t_dur_hrs")
                dur_mins = col_min.selectbox("minutes", options=minute_options, index=0, key="add_t_dur_mins")
                
                duration_hours = int(dur_hours) + (int(dur_mins) / 60.0)
                
                st.divider()
                
                col_o1, col_o2 = st.columns(2)
                origin_desc = col_o1.text_input("Origin Description", key="add_t_odesc")
                origin_loc = col_o2.text_input("Origin Location", key="add_t_oloc")
                    
                col_d1, col_d2 = st.columns(2)
                dest_desc = col_d1.text_input("Destination Description", key="add_t_ddesc")
                dest_loc = col_d2.text_input("Destination Location", key="add_t_dloc")
                
                st.divider()
                
                transit_cost = 0.0
                if needs_booking and is_booked:
                    transit_cost = st.number_input("💰 Transit Cost (₪)", min_value=0.0, value=0.0, step=10.0, key="add_t_cost")
                
                transit_notes = st.text_area("📝 Notes", key="add_t_notes")
                
                st.write("")
                if st.button("Add Transit", use_container_width=True, type="primary", key="add_t_submit"):
                    if not origin_desc.strip() or not dest_desc.strip():
                        st.error("Please enter both origin and destination descriptions.")
                    elif transit_time is None:
                        st.error("Please select a departure time.")
                    elif not (t_start <= transit_date <= t_end):
                        st.error(f"Error: Date must be within trip bounds ({t_start.strftime('%d/%m/%Y')} - {t_end.strftime('%d/%m/%Y')})")
                    else:
                        transit_name = f"{origin_desc.strip()} ➔ {dest_desc.strip()}"
                        
                        new_transit_item = {
                            "name": transit_name,
                            "date": str(transit_date),
                            "time": str(transit_time),
                            "duration": duration_hours,
                            "origin_desc": origin_desc.strip(),
                            "origin_loc": origin_loc.strip(),
                            "dest_desc": dest_desc.strip(),
                            "dest_loc": dest_loc.strip(),
                            "coords": dest_loc.strip() if dest_loc.strip() else dest_desc.strip(), 
                            "budget": transit_cost if (needs_booking and is_booked) else 0.0,
                            "needs_booking": needs_booking,
                            "booked": is_booked if needs_booking else False,
                            "notes": transit_notes.strip(),
                            "type": "transit"
                        }
                        
                        target_day_str = str(transit_date)
                        if "days_metadata" not in v_meta: v_meta["days_metadata"] = {}
                        if target_day_str not in v_meta["days_metadata"]: v_meta["days_metadata"][target_day_str] = {"notes_list": [], "schedule": []}
                        if "schedule" not in v_meta["days_metadata"][target_day_str]: v_meta["days_metadata"][target_day_str]["schedule"] = []
                        
                        v_meta["days_metadata"][target_day_str]["schedule"].append(new_transit_item)
                        save_vacation_meta(v_meta)
                        
                        if add_needs_key in st.session_state: del st.session_state[add_needs_key]
                        if add_booked_key in st.session_state: del st.session_state[add_booked_key]
                        
                        st.success("Transit added successfully!")
                        st.rerun()

        # אופציה 3: הוספת מסעדה
        elif add_choice == "Restaurant":
            with st.form("form_add_restaurant_unique"):
                st.markdown("##### Restaurant Details")
                rest_name = st.text_input("Restaurant Name")
                
                col_d, col_h, col_m = st.columns([1, 0.5, 0.5], vertical_alignment="center")
                
                with col_d:
                    reservation_date = st.date_input("Reservation Date", value=current_nav_date, format="DD/MM/YYYY", key="add_t_date")

                with col_h:
                    reservation_hour = st.selectbox("Hour", options=hour_options, index=10, key="add_t_hour")

                with col_m:
                    reservation_minute = st.selectbox("Minute", options=minute_options, index=0, key="add_t_minute")

                rest_time = time(int(reservation_hour), int(reservation_minute))

                col_lbl, col_hr, col_min = st.columns([0.4, 1, 1], vertical_alignment="center")
                            
                with col_lbl:
                    st.markdown("<div style='margin-top: 10px; font-size: 0.85rem; font-weight: 400;'>Duration:</div>", unsafe_allow_html=True)  
                current_val = float(item.get('duration', 1.0)) if 'item' in locals() and item else 1.0
                def_hrs = int(current_val)
                def_mins = int(round((current_val - def_hrs) * 60))
                
                dur_hours = col_hr.number_input("hours", min_value=0, max_value=24, value=def_hrs, step=1, key=f"d_hrs_{id(item) if 'item' in locals() else 'add'}")
                
                def_mins_str = f"{def_mins:02d}" if def_mins in range(60) else "00"
                min_index = minute_options.index(def_mins_str) if def_mins_str in minute_options else 0
                
                dur_mins = col_min.selectbox("minutes", options=minute_options, index=min_index, key=f"d_mins_{id(item) if 'item' in locals() else 'add'}")
                
                duration_hours = int(dur_hours) + (int(dur_mins) / 60.0)
                
                rest_coords = st.text_input("📍 Address")
                is_booked = st.checkbox("✅ Table Booked / Reserved?", value=False)
                rest_notes = st.text_area("📝 Notes")
                
                if st.form_submit_button("Add Restaurant", use_container_width=True, type="primary"):
                    if not rest_name.strip():
                        st.error("Please enter a restaurant name.")
                    elif rest_time is None:
                        st.error("Please select a start time.")
                    elif not (t_start <= reservation_date <= t_end):
                        st.error(f"Error: Date must be within trip bounds ({t_start.strftime('%d/%m/%Y')} - {t_end.strftime('%d/%m/%Y')})")
                    else:
                        new_rest_item = {
                            "date": str(reservation_date) ,
                            "name": rest_name.strip(),
                            "time": str(rest_time),
                            "duration": duration_hours,
                            "coords": rest_coords.strip(),
                            "booked": is_booked,
                            "budget": 0.0,  
                            "notes": rest_notes.strip(),
                            "type": "restaurant"
                        }
                        
                        target_day_str = str(reservation_date)
                        
                        if "days_metadata" not in v_meta: v_meta["days_metadata"] = {}
                        if target_day_str not in v_meta["days_metadata"]: v_meta["days_metadata"][target_day_str] = {"notes_list": [], "schedule": []}
                        if "schedule" not in v_meta["days_metadata"][target_day_str]: v_meta["days_metadata"][target_day_str]["schedule"] = []
                        
                        v_meta["days_metadata"][target_day_str]["schedule"].append(new_rest_item)
                        save_vacation_meta(v_meta)
                        st.success("Restaurant added successfully!")
                        st.rerun()

        # אופציה 4: הוספת עסקה 
        elif add_choice == "Trip Expense (Shopping, Restaurant, etc.)":
            with st.form("form_add_expense_unique"):
                st.markdown("##### Add Trip Expense")
                
                exp_date = st.date_input("Expense Date", value=current_nav_date, format="DD/MM/YYYY")
                exp_type = st.selectbox("Expense Type", ["Shopping", "Restaurants", "Transportation", "Attractions", "Other"])
                exp_desc = st.text_input("Description (e.g., Souvenir, Ramen shop)")
                exp_amount = st.number_input("Amount (ILS)", min_value=0.0, step=10.0)
                
                if st.form_submit_button("Add to Expenses", use_container_width=True, type="primary"):
                    if exp_amount > 0:
                        expenses_file = f"{project_folder}/trip_expenses.csv"
                        if os.path.exists(expenses_file):
                            df_exp = pd.read_csv(expenses_file)
                        else:
                            df_exp = pd.DataFrame(columns=["ID", "Date", "Expense Type", "Description", "Amount"])
                            
                        if "ID" not in df_exp.columns or df_exp["ID"].isna().any():
                            df_exp["ID"] = range(len(df_exp))
                            
                        new_row = pd.DataFrame([{
                            "ID": int(df_exp["ID"].max() + 1) if not df_exp.empty else 0,
                            "Date": str(exp_date),
                            "Expense Type": exp_type,
                            "Description": exp_desc.strip() if exp_desc else "...",
                            "Amount": exp_amount
                        }])
                        df_exp = pd.concat([df_exp, new_row], ignore_index=True)
                        df_exp.to_csv(expenses_file, index=False)
                        st.success("Expense added to tracker successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter a valid amount.")

    @st.dialog("✏️ Edit Transit")
    def edit_transit_dialog(v_meta, day_key, idx, item):
        with st.container(border=True):
            st.markdown('<div class="focus-trap" tabindex="0"></div>', unsafe_allow_html=True)        
            day_str = str(day_key)
            
            try:
                t_start = datetime.strptime(v_meta.get("start_date", str(date.today())), "%Y-%m-%d").date()
                t_end = datetime.strptime(v_meta.get("end_date", str(date.today() + timedelta(days=7))), "%Y-%m-%d").date()
            except:
                t_start, t_end = date.today(), date.today() + timedelta(days=7)

            try:
                def_res_date = datetime.strptime(item.get('date', day_str), "%Y-%m-%d").date()
            except:
                def_res_date = current_nav_date
            
            state_key_needs = f"edit_needs_bk_{day_str}_{idx}"
            state_key_booked = f"edit_is_bk_{day_str}_{idx}"
            
            if state_key_needs not in st.session_state:
                st.session_state[state_key_needs] = item.get('needs_booking', False)
            if state_key_booked not in st.session_state:
                st.session_state[state_key_booked] = item.get('booked', False)

            needs_booking = st.checkbox(
                "🎟️ Needs to be booked in advance?", 
                value=st.session_state[state_key_needs],
                key=f"chk_needs_{day_str}_{idx}",
                on_change=lambda: st.session_state.update({state_key_needs: st.session_state[f"chk_needs_{day_str}_{idx}"]})
            )

            is_booked = False
            if needs_booking:
                is_booked = st.checkbox(
                    "✅ Already Booked / Reserved?", 
                    value=st.session_state[state_key_booked],
                    key=f"chk_booked_{day_str}_{idx}",
                    on_change=lambda: st.session_state.update({state_key_booked: st.session_state[f"chk_booked_{day_str}_{idx}"]})
                )

            st.markdown("##### Edit Transit Details")
            
            try:
                def_time = datetime.strptime(item.get('time', '10:00:00'), "%H:%M:%S").time()
            except:
                def_time = datetime.strptime("10:00:00", "%H:%M:%S").time()
                
            col_d, col_h, com_m = st.columns([1, 0.5, 0.5], vertical_alignment="center")
            with col_d:
                transit_date = st.date_input("Transit Date", value=def_res_date, format="DD/MM/YYYY", key=f"t_date_{day_str}_{idx}")
            with col_h:
                curr_hr_str = f"{def_time.hour:02d}"
                hr_idx = hour_options.index(curr_hr_str) if curr_hr_str in hour_options else 0
                transit_hour = st.selectbox("Hour", options=hour_options, index=hr_idx, key=f"t_hr_{day_str}_{idx}")
            with com_m:
                curr_min_str = f"{def_time.minute:02d}"
                min_idx = minute_options.index(curr_min_str) if curr_min_str in minute_options else 0
                transit_minute = st.selectbox("Minute", options=minute_options, index=min_idx, key=f"t_min_{day_str}_{idx}")

            transit_time = time(int(transit_hour), int(transit_minute))
            
            curr_dur_val = float(item.get('duration', 1.0))
            def_hrs = int(curr_dur_val)
            def_mins = int(round((curr_dur_val - def_hrs) * 60))

            col_lbl, col_hr, col_min = st.columns([0.4, 1, 1], vertical_alignment="center")
            with col_lbl:
                st.markdown("<div style='margin-top: 10px; font-size: 0.85rem; font-weight: 400; text-align: center;'>Duration:</div>", unsafe_allow_html=True)
                
            dur_hours = col_hr.number_input("hours", min_value=0, max_value=24, value=def_hrs, step=1, key=f"t_hrs_{day_str}_{idx}")
            
            def_mins_str = f"{def_mins:02d}" if def_mins in range(60) else "00"
            dur_min_idx = minute_options.index(def_mins_str) if def_mins_str in minute_options else 0
            dur_mins = col_min.selectbox("minutes", options=minute_options, index=dur_min_idx, key=f"t_mins_{day_str}_{idx}")
            
            transit_duration_hours = int(dur_hours) + (int(dur_mins) / 60.0)
            
            st.divider()
            
            col_o1, col_o2 = st.columns(2)
            origin_desc = col_o1.text_input("Origin Description", value=item.get('origin_desc', ''), key=f"t_odesc_{day_str}_{idx}")
            origin_loc = col_o2.text_input("Origin Location", value=item.get('origin_loc', ''), key=f"t_oloc_{day_str}_{idx}")
                
            col_d1, col_d2 = st.columns(2)
            dest_desc = col_d1.text_input("Destination Description", value=item.get('dest_desc', ''), key=f"t_ddesc_{day_str}_{idx}")
            dest_loc = col_d2.text_input("Destination Location", value=item.get('dest_loc', ''), key=f"t_dloc_{day_str}_{idx}")
            
            st.divider()
            
            transit_cost = float(item.get('budget', 0.0))
            if needs_booking and is_booked:
                transit_cost = st.number_input("💰 Transit Cost (₪)", min_value=0.0, value=transit_cost, step=10.0, key=f"t_cost_{day_str}_{idx}")
            else:
                transit_cost = 0.0
            
            transit_notes = st.text_area("📝 Notes", value=item.get('notes', ''), key=f"t_notes_{day_str}_{idx}")
            
            st.write("")
            col_save, col_del = st.columns(2)
            
            with col_save:
                save_clicked = st.button("Save Changes", use_container_width=True, type="primary", key=f"t_save_{day_str}_{idx}")
            with col_del:
                delete_clicked = st.button("Delete", use_container_width=True, key=f"t_del_{day_str}_{idx}")
            
            if save_clicked:
                if not origin_desc.strip() or not dest_desc.strip():
                    st.error("Please enter both origin and destination descriptions.")
                elif not (t_start <= transit_date <= t_end):
                    st.error(f"❌ Error: Date must be within trip bounds ({t_start.strftime('%d/%m/%Y')} - {t_end.strftime('%d/%m/%Y')})")
                else:
                    target_day_str = str(transit_date)
                    
                    updated_transit_item = {
                        "name": f"{origin_desc.strip()} ➔ {dest_desc.strip()}",
                        "date": target_day_str,
                        "time": str(transit_time),
                        "duration": transit_duration_hours,
                        "origin_desc": origin_desc.strip(),
                        "origin_loc": origin_loc.strip(),
                        "dest_desc": dest_desc.strip(),
                        "dest_loc": dest_loc.strip(),
                        "coords": dest_loc.strip() if dest_loc.strip() else dest_desc.strip(), 
                        "budget": transit_cost if (needs_booking and is_booked) else 0.0,
                        "needs_booking": needs_booking,
                        "booked": is_booked if needs_booking else False,
                        "notes": transit_notes.strip(),
                        "type": "transit"
                    }
                    
                    if "days_metadata" not in v_meta: v_meta["days_metadata"] = {}

                    if target_day_str != day_str:
                        if day_str in v_meta["days_metadata"] and "schedule" in v_meta["days_metadata"][day_str]:
                            if idx < len(v_meta["days_metadata"][day_str]["schedule"]):
                                v_meta["days_metadata"][day_str]["schedule"].pop(idx)
                        
                        if target_day_str not in v_meta["days_metadata"]: 
                            v_meta["days_metadata"][target_day_str] = {"notes_list": [], "schedule": []}
                        if "schedule" not in v_meta["days_metadata"][target_day_str]: 
                            v_meta["days_metadata"][target_day_str]["schedule"] = []
                            
                        v_meta["days_metadata"][target_day_str]["schedule"].append(updated_transit_item)
                    else:
                        if day_str in v_meta["days_metadata"] and "schedule" in v_meta["days_metadata"][day_str]:
                            if idx < len(v_meta["days_metadata"][day_str]["schedule"]):
                                v_meta["days_metadata"][day_str]["schedule"][idx] = updated_transit_item
                    
                    save_vacation_meta(v_meta)
                    
                    if state_key_needs in st.session_state: del st.session_state[state_key_needs]
                    if state_key_booked in st.session_state: del st.session_state[state_key_booked]
                    
                    st.success("Transit updated successfully!")
                    st.rerun()
                    
            if delete_clicked:
                if day_str in v_meta.get("days_metadata", {}):
                    if "schedule" in v_meta["days_metadata"][day_str]:
                        v_meta["days_metadata"][day_str]["schedule"].pop(idx)
                        save_vacation_meta(v_meta)
                        
                        if state_key_needs in st.session_state: del st.session_state[state_key_needs]
                        if state_key_booked in st.session_state: del st.session_state[state_key_booked]
                        
                        st.success("Deleted successfully!")
                        st.rerun()
    
    @st.dialog("✏️ Edit Restaurant")
    def edit_restaurant_dialog(v_meta, day_key, idx, item):
        day_str = str(day_key)

        try:
            t_start = datetime.strptime(v_meta.get("start_date", str(date.today())), "%Y-%m-%d").date()
            t_end = datetime.strptime(v_meta.get("end_date", str(date.today() + timedelta(days=7))), "%Y-%m-%d").date()
        except:
            t_start, t_end = date.today(), date.today() + timedelta(days=7)
        
        try:
            def_res_date = datetime.strptime(item.get('date', day_str), "%Y-%m-%d").date()
        except:
            def_res_date = current_nav_date

        with st.form(f"edit_restaurant_form_{day_str}_{idx}"):
            rest_name = st.text_input("Restaurant Name", value=item.get('name', ''))
            
            try:
                def_time = datetime.strptime(item.get('time', '12:00:00'), "%H:%M:%S").time()
            except:
                def_time = datetime.strptime("12:00:00", "%H:%M:%S").time()

            col_d, col_h, com_m = st.columns([1, 0.5, 0.5], vertical_alignment="center")
                            
            with col_d:
                reservation_date = st.date_input("Reservation Date", value=def_res_date, format="DD/MM/YYYY", key=f"edit_rest_date_{day_str}_{idx}")

            with col_h:
                curr_hr_str = f"{def_time.hour:02d}"
                hr_idx = hour_options.index(curr_hr_str) if curr_hr_str in hour_options else 0
                reservation_hour = st.selectbox("Hour", options=hour_options, index=hr_idx, key=f"edit_rest_hour_{day_str}_{idx}")

            with com_m:
                curr_min_str = f"{def_time.minute:02d}"
                min_idx = minute_options.index(curr_min_str) if curr_min_str in minute_options else 0
                reservation_minute = st.selectbox("Minute", options=minute_options, index=min_idx, key=f"edit_rest_min_{day_str}_{idx}")

            rest_time = time(int(reservation_hour), int(reservation_minute))

            col_lbl, col_hr, col_min = st.columns([0.4, 1, 1], vertical_alignment="center")
                                        
            with col_lbl:
                st.markdown("<div style='margin-top: 10px; font-size: 0.85rem; font-weight: 400;'>Duration:</div>", unsafe_allow_html=True)  
            current_val = float(item.get('duration', 1.0)) if 'item' in locals() and item else 1.0
            def_hrs = int(current_val)
            def_mins = int(round((current_val - def_hrs) * 60))
            
            dur_hours = col_hr.number_input("hours", min_value=0, max_value=24, value=def_hrs, step=1, key=f"d_hrs_{id(item) if 'item' in locals() else 'add'}")
            
            def_mins_str = f"{def_mins:02d}" if def_mins in range(60) else "00"
            min_index = minute_options.index(def_mins_str) if def_mins_str in minute_options else 0
            
            dur_mins = col_min.selectbox("minutes", options=minute_options, index=min_index, key=f"d_mins_{id(item) if 'item' in locals() else 'add'}")
            
            duration_hours = int(dur_hours) + (int(dur_mins) / 60.0)
            
            rest_coords = st.text_input("📍 Address", value=item.get('coords', ''), key=f"edit_rest_addr_{day_str}_{idx}")
            is_booked = st.checkbox("✅ Table Booked / Reserved?", value=item.get('booked', False), key=f"edit_rest_book_{day_str}_{idx}")
            rest_notes = st.text_area("📝 Notes", value=item.get('notes', ''), key=f"edit_rest_notes_{day_str}_{idx}")
            
            col_save, col_del = st.columns(2)
            with col_save:
                save_clicked = st.form_submit_button("Save Changes", use_container_width=True, type="primary")
            with col_del:
                delete_clicked = st.form_submit_button("Delete", use_container_width=True, type="secondary")
            
            if save_clicked:
                target_day_str = str(reservation_date)

                if not (t_start <= reservation_date <= t_end):
                    st.error(f"❌ Error: Date must be within trip bounds ({t_start.strftime('%d/%m/%Y')} - {t_end.strftime('%d/%m/%Y')})")
                    st.stop()

                updated_item = {
                    "date": target_day_str,
                    "name": rest_name.strip(),
                    "time": str(rest_time),
                    "duration": duration_hours,
                    "coords": rest_coords.strip(),
                    "booked": is_booked,
                    "budget": 0.0,
                    "notes": rest_notes.strip(),
                    "type": "restaurant"
                }

                if "days_metadata" not in v_meta: v_meta["days_metadata"] = {}

                if target_day_str != day_str:
                    if day_str in v_meta["days_metadata"] and "schedule" in v_meta["days_metadata"][day_str]:
                        if idx < len(v_meta["days_metadata"][day_str]["schedule"]):
                            v_meta["days_metadata"][day_str]["schedule"].pop(idx)
                    
                    if target_day_str not in v_meta["days_metadata"]: 
                        v_meta["days_metadata"][target_day_str] = {"notes_list": [], "schedule": []}
                    if "schedule" not in v_meta["days_metadata"][target_day_str]: 
                        v_meta["days_metadata"][target_day_str]["schedule"] = []
                        
                    v_meta["days_metadata"][target_day_str]["schedule"].append(updated_item)
                else:
                    if day_str not in v_meta["days_metadata"]: 
                        v_meta["days_metadata"][day_str] = {"notes_list": [], "schedule": []}
                    if "schedule" not in v_meta["days_metadata"][day_str]: 
                        v_meta["days_metadata"][day_str]["schedule"] = []
                        
                    v_meta["days_metadata"][day_str]["schedule"][idx] = updated_item

                save_vacation_meta(v_meta)
                st.success("Updated successfully!")
                st.rerun()
                
            if delete_clicked:
                if day_str in v_meta.get("days_metadata", {}):
                    if "schedule" in v_meta["days_metadata"][day_str]:
                        v_meta["days_metadata"][day_str]["schedule"].pop(idx)
                        save_vacation_meta(v_meta)
                        st.success("Deleted successfully!")
                        st.rerun()

    @st.dialog("Manage Flights")
    def flights_dialog(vac_meta):
        st.markdown("##### Add or Edit Flight Details")
        
        if "flights" not in vac_meta:
            vac_meta["flights"] = []

        def delete_flight_callback(flight_idx):
            if "flights" in vac_meta and 0 <= flight_idx < len(vac_meta["flights"]):
                vac_meta["flights"].pop(flight_idx)
                save_vacation_meta(vac_meta)
            
        with st.form("add_flight_form"):
            col1, col2 = st.columns(2)
            flight_type = col1.selectbox("Flight Direction", ["Outbound", "Return", "Internal / Other"])
            flight_num = col2.text_input("Flight Number (Optional)")
            
            col3, col4 = st.columns(2)
            flight_date = col3.date_input("Outbound date", value=date.today(), format="DD/MM/YYYY")
            
            col_hr1, col_min1 = col4.columns(2)
            dep_hour = col_hr1.selectbox("Hour", options = hour_options, index=10 , key="flight_dep_hr")
            dep_min = col_min1.selectbox("Minute", options = minute_options, index=0, key="flight_dep_min")
            
            col5, col6 = st.columns(2)
            arrival_date = col5.date_input("Arrival Date", value=date.today(), format="DD/MM/YYYY")
            
            col_hr2, col_min2 = col6.columns(2)
            arr_hour = col_hr2.selectbox("Hour", options = hour_options, index=14, key="flight_arr_hr")
            arr_min = col_min2.selectbox("Minute", options= minute_options, index=0, key="flight_arr_min")
            
            flight_price = st.number_input("Price (Optional)", min_value=0.0, value=0.0, step=100.0)
            
            if st.form_submit_button("Add Flight", use_container_width=True, type="primary"):
                dep_time_str = f"{dep_hour}:{dep_min}"
                arr_time_str = f"{arr_hour}:{arr_min}"
                
                f_num_clean = "| " + flight_num.strip() if flight_num.strip() else ""
                
                new_flight = {
                    "type": flight_type,
                    "flight_num": f_num_clean,
                    "date": str(flight_date),
                    "departure_time": dep_time_str,
                    "arrival_date": str(arrival_date),
                    "arrival_time": arr_time_str,
                    "price": flight_price,
                }
                vac_meta["flights"].append(new_flight)
                save_vacation_meta(vac_meta)
                st.success("Flight added successfully!")

        st.markdown("##### Current Flights")
        
        flights = vac_meta.get("flights", [])
        if not flights:
            st.info("No flights added yet.")
        else:
            for idx, f in enumerate(flights):
                col_card, col_del = st.columns([0.94, 0.06], vertical_alignment="center")
                
                try:
                    dep_date_formatted = datetime.strptime(f.get('date', ''), "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    dep_date_formatted = f.get('date', '')
                    
                try:
                    arr_date_formatted = datetime.strptime(f.get('arrival_date', ''), "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    arr_date_formatted = f.get('arrival_date', '')

                with col_card:
                    st.markdown(f"""
                        <div class="flight-card" style="margin-bottom: 0px;">
                            <b>{f.get('type')}</b>  {f.get('flight_num')} <br>
                            {dep_date_formatted} {f.get('departure_time')} ➔ {arr_date_formatted} {f.get('arrival_time')} | {f.get('price'):,.2f}₪  
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col_del:
                    st.markdown("<div style='margin-top: 8px;'>", unsafe_allow_html=True)
                    st.button("🗑️", key=f"del_flight_{idx}", use_container_width=True, help="Delete flight", on_click=delete_flight_callback, args=(idx,))
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.write("")

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
            
            icon = "📁" 
            if proj["type"] == "Vacation Planner":
                v_folder = f"{user_data_dir}/project_{proj['id']}"
                vacation_meta_file = f"{v_folder}/vacation_meta.json"
                
                if os.path.exists(vacation_meta_file):
                    with open(vacation_meta_file, "r", encoding="utf-8") as f:
                        vac_meta = json.load(f)
                        
                        countries = vac_meta.get("countries", [])
                        if not countries and "country" in vac_meta and vac_meta["country"] != "Select Country...":
                            countries = [vac_meta["country"]]
                        
                        if len(countries) == 1:
                            icon = country_emojis.get(countries[0], "✈️")
                        elif len(countries) > 1:
                            icon = "🌍"
                        else:
                            icon = "✈️"
                else:
                    icon = "✈️"
            else:
                icons = {
                    "Monthly Cash Flow Management": "📊",
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
                print("Saving vacation meta to:", vacation_meta_file)  
                with open(vacation_meta_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            vac_meta = load_vacation_meta()

            if st.session_state.get("open_dialog") == "edit_settings":
                st.session_state["open_dialog"] = None
                edit_trip_settings_dialog(vac_meta)
            elif st.session_state.get("open_dialog") == "overview":
                st.session_state["open_dialog"] = None
                trip_overview_dialog(vac_meta, project_folder)
            elif st.session_state.get("open_dialog") == "expenses":
                st.session_state["open_dialog"] = None
                trip_expenses_dialog(project_folder, vac_meta)
            elif st.session_state.get("open_dialog") == "flights":
                st.session_state["open_dialog"] = None
                flights_dialog(vac_meta)

            selected_countries = vac_meta.get("countries", [])
            if not selected_countries and "country" in vac_meta and vac_meta["country"] != "Select Country...":
                selected_countries = [vac_meta["country"]]

            #-------------------------------------
            # שלב א': בחירת מדינות לחופשה
            #-------------------------------------

            if not selected_countries:
                st.markdown("""
                    <div style='text-align: center; margin-top: 40px; margin-bottom: 30px;'>
                        <h2 style='font-size: 2.8rem; font-weight: 800;'>✈️ Planning a New Adventure? 🌴</h2>
                        <p style='font-size: 1.2rem; color: #6c757d;'>Select destination country or countries for this trip.</p>
                    </div>
                """, unsafe_allow_html=True)

                col_space1, col_center, col_space2 = st.columns([1, 2, 1])
                with col_center:
                    chosen_countries = st.multiselect(
                        "Where are we flying to?",
                        options=countries_list,
                        key=f"countries_multiselect_{current_project['id']}"
                    )
                    
                    st.write("")
                    if st.button("Set Destinations & Continue 🚀", use_container_width=True, type="primary"):
                        if not chosen_countries:
                            st.error("Please select at least one destination country.")
                        else:
                            vac_meta["countries"] = chosen_countries
                            save_vacation_meta(vac_meta)
                            st.rerun()

            #-----------------------------------------
            # שלב ב': הגדרת תאריכים ותקציב
            #-----------------------------------------

            elif "start_date" not in vac_meta or "end_date" not in vac_meta:
                countries_str = ", ".join(selected_countries)

                st.markdown(f"""
                    <div style='text-align: center; margin-top: 20px; margin-bottom: 30px;'>
                        <h1 style='margin: 0; font-size: 3rem; font-weight: 900; letter-spacing: 2px;'>🌍 {countries_str.upper()}</h1>
                    </div>
                """, unsafe_allow_html=True)

                col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
                with col_b2:
                    if st.button("🔄 Change Countries", use_container_width=True, type="secondary"):
                        vac_meta["countries"] = []
                        if "country" in vac_meta:
                            del vac_meta["country"]
                        if "segments" in vac_meta:
                            del vac_meta["segments"]
                        save_vacation_meta(vac_meta)
                        st.rerun()

                st.divider()

                st.markdown("<h4 style='margin-bottom: 15px; text-align: center;'>Trip Parameters & Logistics</h4>", unsafe_allow_html=True)

                with st.form(f"vacation_details_form_{current_project['id']}"):
                    if len(selected_countries) == 1:
                        trip_dates = st.date_input("🗓️ Trip Dates (Start & End)", value=(date.today(), date.today() + dt.timedelta(days=1)))
                    
                    col_det1, col_det2 = st.columns(2)
                    with col_det1:
                        travelers_count = st.number_input("Number of Travelers", min_value=1, value=2, step=1)
                    with col_det2:
                        total_budget = st.number_input("Total Budget (ILS)", min_value=0.0, value=10000.0, step=500.0)

                    segments_data = []
                    if len(selected_countries) > 1:
                        st.markdown("---")
                        st.markdown("##### Trip Segments (Multi-Country Split):")
                        
                        if f"num_segments_{current_project['id']}" not in st.session_state:
                            st.session_state[f"num_segments_{current_project['id']}"] = 1
                            
                        num_segs = st.session_state[f"num_segments_{current_project['id']}"]
                        prev_seg_end = date.today()
                        
                        for s in range(num_segs):
                            st.markdown(f"**Segment {s+1}**")
                            
                            default_s_start = date.today() if s == 0 else prev_seg_end
                            default_s_end = default_s_start + dt.timedelta(days=1)
                            
                            s_col1, s_col2 = st.columns([2, 1])
                            with s_col1:
                                seg_dates = st.date_input(f"Dates (Segment {s+1})", value=(default_s_start, default_s_end), key=f"seg_dates_{s}")
                            with s_col2:
                                s_country = st.selectbox(f"Country", options=selected_countries, key=f"seg_country_{s}")
                            
                            if len(seg_dates) == 2:
                                prev_seg_end = seg_dates[1]
                                
                            segments_data.append({"dates": seg_dates, "country": s_country})
                            
                        if st.form_submit_button("➕ Add Another Segment"):
                            st.session_state[f"num_segments_{current_project['id']}"] += 1
                            st.rerun()

                    if st.form_submit_button("Save Vacation Settings & Open Itinerary 🚀", use_container_width=True, type="primary"):
                        if len(selected_countries) > 1:
                            if not segments_data:
                                st.error("Please define at least one segment.")
                                st.stop()
                                
                            final_segments = []
                            all_starts, all_ends = [], []
                            
                            for seg in segments_data:
                                if len(seg["dates"]) < 2:
                                    st.error("Please select BOTH a start and end date for all segments.")
                                    st.stop()
                                s_st, s_en = seg["dates"][0], seg["dates"][1]
                                final_segments.append({"start": str(s_st), "end": str(s_en), "country": seg["country"]})
                                all_starts.append(s_st)
                                all_ends.append(s_en)
                                
                            trip_start = min(all_starts)
                            trip_end = max(all_ends)
                            vac_meta["segments"] = final_segments
                        else:
                            if len(trip_dates) < 2:
                                st.error("Please select BOTH a start and end date.")
                                st.stop()
                            trip_start, trip_end = trip_dates[0], trip_dates[1]
                            vac_meta["segments"] = [{"start": str(trip_start), "end": str(trip_end), "country": selected_countries[0]}]

                        if trip_start > trip_end:
                            st.error("Start date cannot be after end date.")
                        else:
                            vac_meta["start_date"] = str(trip_start)
                            vac_meta["end_date"] = str(trip_end)
                            vac_meta["travelers"] = travelers_count
                            vac_meta["budget"] = total_budget
                            vac_meta["current_trip_date"] = str(trip_start)
                            
                            if "days_metadata" not in vac_meta:
                                vac_meta["days_metadata"] = {}

                            for seg in vac_meta["segments"]:
                                s_dt = datetime.strptime(seg["start"], "%Y-%m-%d").date()
                                e_dt = datetime.strptime(seg["end"], "%Y-%m-%d").date()
                                c_name = seg["country"]
                                
                                curr = s_dt
                                while curr <= e_dt:
                                    d_key = str(curr)
                                    if d_key not in vac_meta["days_metadata"]:
                                        vac_meta["days_metadata"][d_key] = {}
                                    vac_meta["days_metadata"][d_key]["country"] = c_name
                                    curr += dt.timedelta(days=1)

                            save_vacation_meta(vac_meta)
                            st.rerun()

            #-------------------------------------
            # שלב ג': מסך החופשה הראשי
            #-------------------------------------

            else:
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
                current_day_key = str(current_nav_date)

                default_c = selected_countries[0] if selected_countries else "Japan"
                if "days_metadata" not in vac_meta: vac_meta["days_metadata"] = {}
                if current_day_key not in vac_meta["days_metadata"]: vac_meta["days_metadata"][current_day_key] = {}
                
                day_country = vac_meta["days_metadata"][current_day_key].get("country", default_c)
                if day_country not in selected_countries and selected_countries:
                    day_country = selected_countries[0]

                flag_emoji = country_emojis.get(day_country, "🌍")

                col_c1, col_c2, col_c3 = st.columns([1, 4, 1])
                with col_c2:
                    if st.button(f"{flag_emoji}  {day_country.upper()}  {flag_emoji}", key="pure_title_btn", use_container_width=True, help="Click to open trip menu"):
                        trip_menu_dialog(vac_meta, project_folder)

                st.divider()
                
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
            
                if "days_metadata" not in vac_meta: vac_meta["days_metadata"] = {}
                if current_day_key not in vac_meta["days_metadata"]: 
                    vac_meta["days_metadata"][current_day_key] = {"notes_list": [], "schedule": []}
                if "schedule" not in vac_meta["days_metadata"][current_day_key]:
                    vac_meta["days_metadata"][current_day_key]["schedule"] = []

                current_day_meta = vac_meta["days_metadata"][current_day_key]
                day_schedule = vac_meta["days_metadata"][current_day_key]["schedule"]

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
                            item_type = item.get('type', 'attraction')
                            
                            if item_type == 'transit':
                                border_color = "#29b6f6"  
                            elif item_type == 'restaurant':
                                border_color = "#ef5350" 
                            else:
                                border_color = "#66bb6a"  
                            
                            with st.container(border=True):
                                st.markdown(f"""
                                    <style>
                                        div[data-testid='stVerticalBlock']:has(> div.element-container .card-marker-{idx}) {{
                                            border: 2px solid {border_color} !important;
                                            border-radius: 10px !important;
                                        }}
                                        div[data-testid='stVerticalBlock']:has(> div.element-container .card-marker-{idx}) div.stVerticalBlock {{
                                            gap: 0rem !important;
                                            margin-top: -17px
                                        }}
                                    </style>
                                    <div class="card-marker-{idx}" style="display:none; margin:0; padding:0;"></div>
                                """, unsafe_allow_html=True)
                                
                                if item_type == 'transit':
                                    needs_booking = item.get('needs_booking', False)
                                    is_booked = item.get('booked', False)
                                    cost = item.get('budget', 0)
                                    
                                    c_time, c_info, c_cost, c_map, c_edit = st.columns([0.15, 0.55, 0.2, 0.05, 0.05], vertical_alignment="center")
                                    
                                    with c_time:
                                        dep_time = item.get('time', '00:00')[:5]
                                        st.markdown(f"""
                                            <div style='text-align: center; margin-bottom: 34px; display: flex; flex-direction: column; justify-content: center; height: 100%;'>
                                                <div style='font-size: 0.75rem; opacity: 0.6; font-weight: 500; margin-bottom: 2px;'>Departure</div>
                                                <div style='font-size: 1.25rem; font-weight: 800; line-height: 1.2;'>{dep_time}</div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                                    with c_info:
                                        orig_desc = item.get('origin_desc', 'Origin')
                                        orig_loc = item.get('origin_loc', '')
                                        dest_desc = item.get('dest_desc', 'Destination')
                                        dest_loc = item.get('dest_loc', '')
                                        dur_formatted = format_duration(item.get('duration', 1.0))
                                        
                                        st.markdown(f"""
                                            <div style='text-align: center; margin-bottom: 17px;'>
                                                <div style='font-size: 1.0rem; font-weight: 700;'>{orig_desc}</div>
                                                <div style='font-size: 0.75rem; opacity: 0.7;'>{orig_loc}</div>
                                                <div class="attr-duration" style='text-align: center; color: #c62828; margin: 4px auto; display: inline-block;'>Duration:<br><b>{dur_formatted}</b></div>
                                                <div style='font-size: 1.0rem; font-weight: 700;'>{dest_desc}</div>
                                                <div style='font-size: 0.75rem; opacity: 0.7;'>{dest_loc}</div>
                                            </div>
                                        """, unsafe_allow_html=True)

                                    with c_cost:
                                        if needs_booking:
                                            if is_booked:
                                                st.markdown(f"<div style='text-align: center; margin-bottom: 17px; font-weight: 800;'>₪{cost}</div>", unsafe_allow_html=True)
                                            else:
                                                st.markdown(f"<div style='text-align: center; margin-bottom: 17px; font-size: 0.85rem; color: #d32f2f; font-weight: 600;'>Not Booked</div>", unsafe_allow_html=True)
                                        else:
                                            st.markdown("<div style='text-align: center; margin-bottom: 17px;'></div>", unsafe_allow_html=True)
                                        
                                    with c_map:
                                        orig_target = item.get('origin_loc') if item.get('origin_loc') else orig_desc
                                        dest_target = item.get('dest_loc') if item.get('dest_loc') else dest_desc
                                        gmap_url = f"https://www.google.com/maps/dir/?api=1&origin={orig_target.strip().replace(' ', '+')}&destination={dest_target.strip().replace(' ', '+')}"
                                        
                                        st.markdown(f"""
                                            <div style='text-align: center; margin-bottom: 17px;'>
                                                <a href='{gmap_url}' target='_blank' class='hover-scale' style='font-size: 1.2rem; text-decoration: none;' title='Navigate'>📍</a>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                                    with c_edit:
                                        st.markdown("<div class='hover-scale' style='text-align: center;'>", unsafe_allow_html=True)
                                        if st.button("✏️", key=f"edit_transit_{current_day_key}_{idx}", help="Edit Transit"):
                                            edit_transit_dialog(vac_meta, current_day_key, idx, item)
                                        st.markdown("<div style='text-align: center; margin-bottom: 28px;'></div>", unsafe_allow_html=True)

                                elif item_type == 'restaurant':
                                    c_time, c_info, c_booked, c_map, c_edit = st.columns([0.15, 0.55, 0.2, 0.05, 0.05], vertical_alignment="center")
                                    start_time_str = item['time'][:5]
                                    dur_formatted = format_duration(item.get('duration', 1.0))
                                    rest_name = item.get('name', 'Restaurant')
                                    rest_notes = item.get('notes', '')
                                    is_booked = item.get('booked', False)
                                    loc_display = item.get('coords', '')
                                    
                                    with c_time:
                                        st.markdown(f"""
                                            <div style='text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%;'>
                                                <span style='font-size: 1.25rem; font-weight: 800; display: block; text-align: center; margin-bottom: -10px;'>{start_time_str}</span>
                                                <div style='display: flex; justify-content: center; width: 100%; margin-bottom: 10px;'>
                                                    <div class="attr-duration" style='text-align: center; font-size: 0.6rem; display: inline-block; transform: translateX(-3px);'>Duration:<br><b>{dur_formatted}</b></div>
                                                </div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                                    with c_info:
                                        st.markdown(f"""
                                            <div style='text-align: center;'>
                                                <div style='font-size: 1.0rem; font-weight: 700;'>{rest_name}</div>
                                                <div style='font-size: 0.75rem; opacity: 0.7; margin-bottom: 15px;'>{rest_notes}</div>
                                            </div>
                                        """, unsafe_allow_html=True)

                                    with c_booked:
                                        booked_badge = "<span style='color: #2e7d32; font-weight: 800;'>✓ Booked</span>" if is_booked else "<span style='color: #d32f2f; font-weight: 600;'>Not Booked</span>"
                                        st.markdown(f"<div style='text-align: center; margin-bottom: 15px; font-size: 0.9rem;'>{booked_badge}</div>", unsafe_allow_html=True)
                                        
                                    with c_map:
                                        map_target = loc_display if loc_display else rest_name
                                        gmap_url = f"https://www.google.com/maps/search/?api=1&query={map_target.strip().replace(' ', '+')}"
                                        st.markdown(f"""
                                            <div style='text-align: center; margin-bottom: 15px;'>
                                                <a href='{gmap_url}' target='_blank' class='hover-scale' style='font-size: 1.2rem; text-decoration: none;' title='View location in Google Maps'>📍</a>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with c_edit:
                                        st.markdown("<div style='margin-bottom: -100px;'></div>", unsafe_allow_html=True)
                                        if st.button("✏️", key=f"edit_rest_{current_day_key}_{idx}", help="Edit Restaurant"):
                                            edit_restaurant_dialog(vac_meta, current_day_key, idx, item)

                                else:
                                    needs_booking = item.get('needs_booking', False)
                                    is_booked = item.get('booked', False)
                                    cost = item.get('budget', 0)
                                    
                                    c_time, c_info, c_cost, c_map, c_edit = st.columns([0.15, 0.55, 0.2, 0.05, 0.05], vertical_alignment="center")
                                    
                                    with c_time:
                                        dur_formatted = format_duration(item.get('duration', 1.0))
                                        st.markdown(f"""
                                            <div style='text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; width: 100%;'>
                                                <span style='font-size: 1.25rem; font-weight: 800; display: block; text-align: center; margin-bottom: -10px;'>{item['time'][:5]}</span>
                                                <div style='display: flex; justify-content: center; width: 100%; margin-bottom: 10px;'>
                                                    <div class="attr-duration" style='text-align: center; font-size: 0.6rem; display: inline-block; transform: translateX(-3px);'>Duration:<br><b>{dur_formatted}</b></div>
                                                </div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                        
                                    with c_info:
                                        st.markdown(f"""
                                            <div style='text-align: center;'>
                                                <div style='font-size: 1.0rem; font-weight: 700;'>{item.get('name', 'Attraction')}</div>
                                                <div style='font-size: 0.75rem; opacity: 0.7; margin-bottom: 15px;'>{item.get('notes', '')}</div>
                                            </div>
                                        """, unsafe_allow_html=True)

                                    with c_cost:
                                        if needs_booking:
                                            if is_booked:
                                                st.markdown(f"<div style='text-align: center; margin-bottom: 15px; font-weight: 800;'>₪{cost}</div>", unsafe_allow_html=True)
                                            else:
                                                st.markdown(f"<div style='text-align: center; margin-bottom: 15px; font-size: 0.85rem; color: #d32f2f; font-weight: 600;'>Not Booked</div>", unsafe_allow_html=True)
                                        else:
                                            st.markdown("<div style='text-align: center; margin-bottom: 15px;'></div>", unsafe_allow_html=True)
                                        
                                    with c_map:
                                        loc_display = item.get('coords', item.get('location', ''))
                                        map_target = loc_display if loc_display else item.get('name', 'Attraction')
                                        gmap_url = f"https://www.google.com/maps/search/?api=1&query={map_target.strip().replace(' ', '+')}"
                                        st.markdown(f"""
                                            <div style='text-align: center; margin-bottom: 15px;'>
                                                <a href='{gmap_url}' target='_blank' class='hover-scale' style='font-size: 1.2rem; text-decoration: none;' title='View location in Google Maps'>📍</a>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    
                                    with c_edit:
                                        st.markdown("<div style='margin-bottom: -100px;'></div>", unsafe_allow_html=True)
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

                    # =============== מפה ומסלול יומי ===============
                    with row2_c2:
                        with st.container(border=True):
                            st.markdown("<div style='font-size: 1.1rem; font-weight: bold; margin-bottom: 8px;'>🗺️ Map & Daily Route</div>", unsafe_allow_html=True)
                            
                            schedule = vac_meta.get("days_metadata", {}).get(str(current_day_key), {}).get("schedule", [])
                            if schedule:
                                schedule = sorted(schedule, key=lambda x: x['time'])

                            hotels_list = vac_meta.get("hotels", [])
                            active_hotel = None
                            for h in hotels_list:
                                if h["check_in"] <= current_day_key < h["check_out"]:
                                    active_hotel = h
                                    break
                            
                            if active_hotel and active_hotel.get('address'):
                                map_location = active_hotel['address']
                            else:
                                map_location = day_country
                            
                            embed_url = f"https://www.google.com/maps?q={map_location.strip().replace(' ', '+')}&output=embed"
                            st.components.v1.iframe(embed_url, height=150, scrolling=False)
                            
                            attraction_locations = []
                            for item in schedule:
                                if item.get("type") == "transit":
                                    continue
                                loc = item.get("coords") or item.get("location") or item.get("name")
                                if loc and loc.strip():
                                    attraction_locations.append(loc.strip())
                            
                            if attraction_locations:
                                if len(attraction_locations) == 1:
                                    single_target = attraction_locations[0]
                                    gmaps_route_link = f"https://www.google.com/maps/search/?api=1&query={single_target.replace(' ', '+')}"
                                else:
                                    origin = attraction_locations[0]
                                    destination = attraction_locations[-1]
                                    waypoints = attraction_locations[1:-1]
                                    
                                    base_dir_url = f"https://www.google.com/maps/dir/?api=1&origin={origin.replace(' ', '+')}&destination={destination.replace(' ', '+')}"
                                    if waypoints:
                                        waypoints_str = "|".join([w.replace(' ', '+') for w in waypoints])
                                        base_dir_url += f"&waypoints={waypoints_str}"
                                    
                                    gmaps_route_link = base_dir_url
                            else:
                                fallback_target = active_hotel['address'] if (active_hotel and active_hotel.get('address')) else day_country
                                gmaps_route_link = f"https://www.google.com/maps/search/?api=1&query={fallback_target.replace(' ', '+')}"

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

                            btn_text = "Open Today's Full Route in Google Maps" if len(attraction_locations) > 1 else "📍 View Location in Google Maps"
                            st.link_button(btn_text, gmaps_route_link, use_container_width=True)

                if st.button("➕ Add", key="fab_attraction", help="Add attraction, transit, or expense"):
                    unified_trip_add_dialog(vac_meta, current_nav_date, project_folder)

        # ------------------------------------------------
        # מודול שכר שעה 
        # ------------------------------------------------

        elif current_project["type"] == "Hourly Wage Tracker":
            st.info("Under Development")
        
        # ------------------------------------------------
        # מודול חיסכון 
        # ------------------------------------------------

        elif current_project["type"] == "Goal-Based Savings":
            st.info("Under Development")
