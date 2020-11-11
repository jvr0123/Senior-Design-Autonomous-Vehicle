#include "cMain.h"
//Need to create/find suitable icons
#include "wx/artprov.h"



cMain::cMain() : wxFrame(nullptr, wxID_ANY, "Car Control")
{
	//TODO: decide functionality/layout of menu tabs
	wxMenuBar* menuBar = new wxMenuBar();
	wxMenu* fileMenu = new wxMenu();

	//TODO add actual menu items

	//new menu
	fileMenu->Append(wxID_NEW);

	//template to add more items
	wxMenuItem* todo = new wxMenuItem(fileMenu, wxID_EXECUTE);
	fileMenu->Append(wxID_ANY, _("TODO\tCtrl+T"));
	//if additional options are needed can use subMenu object instead

	fileMenu->AppendSeparator();

	//quit option
	wxMenuItem *quitItem = new wxMenuItem(fileMenu, wxID_EXIT);
	fileMenu->Append(quitItem);
	
	

	menuBar->Append(fileMenu, _("File"));
	SetMenuBar(menuBar);
}

cMain::~cMain()
{

}