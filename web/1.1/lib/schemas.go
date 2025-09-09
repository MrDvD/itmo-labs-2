package lib

import (
	"errors"

	"github.com/graphql-go/graphql"
)

func GetSchemaConfig() (graphql.Schema, error) {
	fields := graphql.Fields{
		"dotParams": &graphql.Field{
			Type: graphql.NewList(DotStatusSchema),
			Args: graphql.FieldConfigArgument{
				"dotParamsArray": &graphql.ArgumentConfig{
					Type: graphql.NewList(graphql.NewNonNull(DotParamsInput)),
				},
			},
			Resolve: func(p graphql.ResolveParams) (interface{}, error) {
				dotParamsArray, ok := p.Args["dotParamsArray"].([]interface{})
				if !ok {
					return nil, errors.New("не удалось распознать аргументы запроса")
				}
				dotStatuses := []DotStatus{}
				for _, rawDot := range dotParamsArray {
					dotInterface, ok := rawDot.(map[string]interface{})
					if !ok {
						return nil, errors.New("не удалось распознать аргументы запроса")
					}
					dot := DotParams{
						X: dotInterface["X"].(string),
						Y: dotInterface["Y"].(float64),
						R: dotInterface["R"].(string),
					}
					dotStatus, err := wrapDotStatus(dot)
					if err != nil {
						return nil, err
					}
					dotStatuses = append(dotStatuses, dotStatus)
				}
				return dotStatuses, nil
			},
		},
	}
	rootQuery := graphql.ObjectConfig{Name: "RootQuery", Fields: fields}
	schemaConfig := graphql.SchemaConfig{Query: graphql.NewObject(rootQuery)}
	return graphql.NewSchema(schemaConfig)
}
