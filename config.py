config = {

    # Run Settings

    "runMessage":"Server Is Running",
    "runWithPort":5050,

    # METHODS

    "todoListMETHOD":["GET"],
    "todoAddMETHOD":["POST"],
    "todoReadByIDMETHOD":["GET"],
    "todoUpdateMETHOD":["POST"],
    "todoDeleteMETHOD":["POST"],

    # Router

    "todoListROUTE":"/api/Todo/list",
    "todoAddROUTE":"/api/Todo/add",
    "todoDeleteROUTE":"/api/Todo/delete/<int:id>",
    "todoReadROUTE":"/api/Todo/<int:id>",
    "todoUpdateROUTE":"/api/Todo/update/<int:id>",

    # REQUIRED

    "titleIsRequired":True,
    "descriptionIsRequired":True,

    # Status Codes

    "done":200,
    "not-found":404,
    "error":400,
    "BadMethod":405,
}
