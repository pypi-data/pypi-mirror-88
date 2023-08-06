/*
 *  gttk_Entry.cpp
 * ------------------
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

#include "gttk_Utilities.h"
#include "gttk_TkHeaders.h"
#include "gttk_WidgetDefaults.h"

#if 0
/*
 * Map between Tk/Tile & Gtk/GNOME state flags.
 */
static Ttk_StateTable entry_statemap[] =
{
};
#endif

typedef struct {
} EntryFieldElement;


static Ttk_ElementOptionSpec EntryFieldElementOptions[] = {
    {NULL}
};

static void EntryFieldElementGeometry(
    void *clientData, void *elementRecord, Tk_Window tkwin,
    int *widthPtr, int *heightPtr, Ttk_Padding *paddingPtr)
{
    GTTK_WIDGET_CACHE_DEFINITION;
    // GtkBorder border = {0, 0, 0, 0};
    GTTK_ENSURE_GTK_STYLE_ENGINE_ACTIVE;
    GtkWidget *widget = gttk_GetEntry(wc);
    GTTK_ENSURE_WIDGET_OK;
    int xt = widget->style->xthickness;
    int yt = widget->style->ythickness;
    *paddingPtr = Ttk_MakePadding(xt + EntryUniformPadding,
                                  yt + EntryUniformPadding,
                                  xt + EntryUniformPadding,
                                  yt + EntryUniformPadding);
    // gttk_gtk_widget_style_get(widget, "inner-border", &border, NULL);
    // gttk_g_object_get(widget, "inner-border", &border, NULL);
    // *paddingPtr = GTTK_GTKBORDER_TO_PADDING(border);
}

static void EntryFieldElementDraw(
    void *clientData, void *elementRecord, Tk_Window tkwin,
    Drawable d, Ttk_Box b, unsigned state)
{
    GTTK_GTK_DRAWABLE_DEFINITIONS;
    GTTK_ENSURE_GTK_STYLE_ENGINE_ACTIVE;
    gboolean hasFrame = TRUE;
    GtkWidget *widget = gttk_GetEntry(wc);
    GTTK_ENSURE_WIDGET_OK;
    GTTK_DRAWABLE_FROM_WIDGET;
    style = gttk_GetGtkWindowStyle(wc->gtkWindow);
    GTTK_DEFAULT_BACKGROUND;
    if (hasFrame) {
      GTTK_STYLE_FROM_WIDGET;
      gttk_StateShadowTableLookup(NULL, state, gtkState, gtkShadow,
              GTTK_SECTION_ENTRY|GTTK_SECTION_ALL);
      gttk_gtk_paint_flat_box(style, gdkDrawable, gtkState, gtkShadow, NULL, widget,
          "entry_bg", 0, 0, b.width, b.height);
      GTTK_WIDGET_SET_FOCUS(widget);
      gttk_gtk_paint_shadow(style, gdkDrawable, gtkState, gtkShadow, NULL,
              widget, "entry", 0, 0, b.width, b.height);
    }
    // gttk_StateInfo(state, gtkState, gtkShadow, tkwin, widget);
    gttk_CopyGtkPixmapOnToDrawable(gdkDrawable, d, tkwin,
                   0, 0, b.width, b.height, b.x, b.y);
    GTTK_CLEANUP_GTK_DRAWABLE;
}

static Ttk_ElementSpec EntryFieldElementSpec = {
    TK_STYLE_VERSION_2,
    sizeof(EntryFieldElement),
    EntryFieldElementOptions,
    EntryFieldElementGeometry,
    EntryFieldElementDraw
};

/*------------------------------------------------------------------------
 * +++ Widget layout.
 */

int gttk_Init_Entry(Tcl_Interp *interp,
                       gttk_WidgetCache **wc, Ttk_Theme themePtr)
{
    /*
     * Register elements:
     */
    Ttk_RegisterElement(interp, themePtr, "Entry.field",
            &EntryFieldElementSpec, (void *) wc[0]);
    
    /*
     * Register layouts:
     */

    return TCL_OK;
}; /* gttk_Init_Entry */
