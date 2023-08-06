/*
 *  gttk_Utilities.h
 * ----------------------
 *
 * This file is part of the gttk package, a Tk/Tile based theme that uses
 * Gtk/GNOME for drawing.
 *
 * Copyright (C) 2004-2008 by:
 * Georgios Petasis, petasis@iit.demokritos.gr,
 * Software and Knowledge Engineering Laboratory,
 * Institute of Informatics and Telecommunications,
 * National Centre for Scientific Research (NCSR) "Demokritos",
 * Aghia Paraskevi, 153 10, Athens, Greece.
 */

#include "gttk_GtkHeaders.h"
#include "gttk_Elements.h"
#include <string.h>

#define NO_GTK_STYLE_ENGINE {/*printf("NULL qApp\n");fflush(NULL);*/return;}

#define GTTK_ENSURE_GTK_STYLE_ENGINE_ACTIVE \
  if (!gttk_GtkInitialised()) return;

#define GTTK_ENSURE_WIDGET_OK \
  if (!widget) return;

#define GTTK_ATTACH_STYLE_TO_WIDGET \
  style = gttk_gtk_style_attach(style, widget->window);

#define GTTK_WIDGET_CACHE_DEFINITION \
  gttk_WidgetCache *wc = (gttk_WidgetCache *) clientData;

#define GTTK_ORIENTATION_DEFINITION \
  int orientation = wc->orientation;

#define GTTK_GTK_DRAWABLE_DEFINITIONS \
  gttk_WidgetCache *wc = (gttk_WidgetCache *) clientData; \
  GdkPixmap    *gdkDrawable = NULL; \
  GtkStyle     *style       = NULL; \
  GtkStateType  gtkState    = GTK_STATE_NORMAL; \
  GtkShadowType gtkShadow   = GTK_SHADOW_NONE;

#define GTTK_SETUP_GTK_DRAWABLE \
  GTTK_SETUP_GTK_DRAWABLE_PIXMAP_SIZE(b.width, b.height)

#define GTTK_SETUP_GTK_DRAWABLE_PIXMAP_SIZE(pw, ph) \
  if (!wc) return; \
  style = gttk_GetGtkWindowStyle(wc->gtkWindow); \
  if (!style) return; \
  gdkDrawable = gttk_gdk_pixmap_new(wc->gtkWindow->window, pw, ph, -1); \
  style = gttk_GetGtkWindowStyle(wc->gtkWindow);

#define GTTK_STYLE_BACKGROUND_DEFAULT \
  if (wc && wc->gtkWindow) style = gttk_GetGtkWindowStyle(wc->gtkWindow); \
  if (!style) return;

#define GTTK_STYLE_FROM_WIDGET \
  style = gttk_GetGtkWindowStyle(widget); \
  if (!style) style = gttk_GetGtkWindowStyle(wc->gtkWindow); \
  if (!style) return;

#define GTTK_DRAWABLE_FROM_WIDGET_SIZE(pw, ph) \
  gdkDrawable = gttk_gdk_pixmap_new(widget->window, pw, ph, -1);

#define GTTK_DRAWABLE_FROM_WIDGET \
  GTTK_DRAWABLE_FROM_WIDGET_SIZE(b.width, b.height)

// #define GTTK_DRAWABLE_FROM_WIDGET \
//   gdkDrawable = gdk_pixmap_foreign_new(Tk_WindowId(tkwin)); \
//   GdkColormap gdkColormap = gdk_x11_colormap_foreign_new(gdkx_visual_get(Tk_Visual(tkwin)), Tk_Colormap(tkwin)); \
//   gdk_drawable_set_colormap(gdkDrawable, gdkColormap);

#define GTTK_DEFAULT_BACKGROUND_SIZE(pw, ph) \
  gttk_gtk_style_apply_default_background(style, gdkDrawable, TRUE, \
               gtkState, NULL, 0, 0, pw, ph);

#define GTTK_DEFAULT_BACKGROUND \
  GTTK_DEFAULT_BACKGROUND_SIZE(b.width, b.height)

#define GTTK_CLEANUP_GTK_DRAWABLE \
  if (gdkDrawable) gttk_g_object_unref(gdkDrawable);

#define GTTK_SETUP_STATE_SHADOW(statemap, shadowmap) \
    gtkState  = (GtkStateType) \
       gttk_StateTableLookup(statemap,  state); \
    gtkShadow = (GtkShadowType) \
       gttk_StateTableLookup(shadowmap, state);

#define GTTK_SETUP_WIDGET_SIZE(width, height) \
  gttk_gtk_widget_set_size_request(widget, width, height);

#define GTTK_GET_WIDGET_SIZE(widthPtr, heightPtr)  \
  if (widget) { \
    GtkRequisition size; \
    gttk_gtk_widget_size_request(widget, &size); \
    widthPtr  = size.width; \
    heightPtr = size.height; \
  }

#define GTTK_WIDGET_SETUP_DEFAULT(obj) \
  int defaultState  = TTK_BUTTON_DEFAULT_DISABLED; \
  int has_default = (defaultState == TTK_BUTTON_DEFAULT_ACTIVE); \
  /*Ttk_GetButtonDefaultStateFromObj(NULL, obj, &defaultState);*/

#ifdef GTTK_LOAD_GTK_DYNAMICALLY

#define GTTK_WIDGET_SET_FOCUS(widget)

#define GTTK_WIDGET_SET_DEFAULT(widget, obj) \
  int defaultState  = TTK_BUTTON_DEFAULT_DISABLED; \
  int has_default = (defaultState == TTK_BUTTON_DEFAULT_ACTIVE);

#else /* GTTK_LOAD_GTK_DYNAMICALLY */

#define GTTK_WIDGET_SET_FOCUS(widget) \
  if (state & TTK_STATE_FOCUS) { \
    GTK_WIDGET_SET_FLAGS(widget,   GTK_HAS_FOCUS); \
  } else { \
    GTK_WIDGET_UNSET_FLAGS(widget, GTK_HAS_FOCUS); \
  }

#define GTTK_WIDGET_SET_DEFAULT(widget, obj) \
  int defaultState  = TTK_BUTTON_DEFAULT_DISABLED; \
  int has_default = (defaultState == TTK_BUTTON_DEFAULT_ACTIVE); \
  /*Ttk_GetButtonDefaultStateFromObj(NULL, obj, &defaultState);*/ \
  if (has_default) { \
    GTK_WIDGET_SET_FLAGS(widget,   GTK_HAS_DEFAULT); \
  } else { \
    GTK_WIDGET_UNSET_FLAGS(widget, GTK_HAS_DEFAULT); \
  } 
#endif /* GTTK_LOAD_GTK_DYNAMICALLY */

#define GTTK_DEBUG_PRINT_BOX \
  printf("x=%d, y=%d, w=%d, h=%d\n", b.x, b.y, b.width, b.height); \
  fflush(0);

#define GTTK_DEBUG_PRINT_TK_WIDGET \
  printf("Widget: %s,p=%p\n", Tk_PathName(tkwin), tkwin); \
  fflush(0);

#define GTTK_GTKBORDER_TO_PADDING(border) \
  Ttk_MakePadding(border.left, border.top, border.right, border.bottom)

TCL_DECLARE_MUTEX(gttkMutex);

/* Global Symbols */

/* Helper Functions */
extern int        gttk_GtkInitialised(void);
extern GtkWidget *gttk_GetGtkWindow(void);
extern GtkStyle  *gttk_GetGtkWindowStyle(GtkWidget *gtkWindow);
extern GtkStyle  *gttk_GetGtkStyle(void);

extern unsigned int gttk_StateTableLookup(Ttk_StateTable *, unsigned int);
extern void gttk_CopyGtkPixmapOnToDrawable(GdkPixmap *, Drawable, Tk_Window,
                                            int, int, int, int, int, int);
extern void gttk_StateInfo(int, GtkStateType,
                    GtkShadowType, Tk_Window, GtkWidget *widget = NULL);

extern GtkWidget *gttk_GetArrow(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetButton(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetCheckButton(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetRadioButton(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetToolBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetToolButton(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetFrame(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetEntry(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetCombobox(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetComboboxEntry(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetHScrollBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetVScrollBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetScrollBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetHScale(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetVScale(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetScale(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetHProgressBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetVProgressBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetProgressBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetStatusBar(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetPaned(gttk_WidgetCache* wc);
extern GtkWidget *gttk_GetNotebook(gttk_WidgetCache* wc);
#if 0
extern void gttk_StoreStyleNameLowers(gttk_WidgetCache *wc);
extern bool gttk_ThemeIs(gttk_WidgetCache *wc, const char* name);
extern void gttk_SetFocus(bool focus);
#endif

extern unsigned int gttk_StateShadowTableLookup(gttk_StateTable*,
       unsigned int, GtkStateType&, GtkShadowType&,
       unsigned int section = GTTK_SECTION_ALL);
extern double gttk_ValueFromSlider(gttk_WidgetCache *wc, Tk_Window tkwin,
                               Ttk_Box b);
