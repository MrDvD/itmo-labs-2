package lib

import "github.com/graphql-go/graphql"

type DotParams struct {
	X string  `json:"X"`
	Y float64 `json:"Y"`
	R string  `json:"R"`
}

type DotStatus struct {
	Entry    DotParams `json:"entry"`
	Hit      bool      `json:"hit"`
	Date     string    `json:"date"`
	Duration string    `json:"duration"`
}

type graphqlPostData struct {
	Query     string                 `json:"query"`
	Operation string                 `json:"operationName"`
	Variables map[string]interface{} `json:"variables"`
}

var DotParamsInput = graphql.NewInputObject(graphql.InputObjectConfig{
	Name: "DotParamsInput",
	Fields: graphql.InputObjectConfigFieldMap{
		"X": &graphql.InputObjectFieldConfig{
			Type: graphql.NewNonNull(graphql.String),
		},
		"Y": &graphql.InputObjectFieldConfig{
			Type: graphql.NewNonNull(graphql.Float),
		},
		"R": &graphql.InputObjectFieldConfig{
			Type: graphql.NewNonNull(graphql.String),
		},
	},
})

var DotParamsSchema = graphql.NewObject(graphql.ObjectConfig{
	Name: "DotParams",
	Fields: graphql.Fields{
		"X": &graphql.Field{
			Type: graphql.NewNonNull(graphql.String),
		},
		"Y": &graphql.Field{
			Type: graphql.NewNonNull(graphql.Float),
		},
		"R": &graphql.Field{
			Type: graphql.NewNonNull(graphql.String),
		},
	},
})

var DotStatusSchema = graphql.NewObject(graphql.ObjectConfig{
	Name: "DotStatus",
	Fields: graphql.Fields{
		"entry": &graphql.Field{
			Type: graphql.NewNonNull(DotParamsSchema),
		},
		"hit": &graphql.Field{
			Type: graphql.NewNonNull(graphql.Boolean),
		},
		"date": &graphql.Field{
			Type: graphql.NewNonNull(graphql.String),
		},
		"duration": &graphql.Field{
			Type: graphql.NewNonNull(graphql.String),
		},
	},
})
