QUERY_RATE_LIMIT = """
    {
      viewer {
        login
      }
      rateLimit {
        limit
        cost
        remaining
        resetAt
      }
    }
    """



QUERY_REPOS = """
      query($selected_repo: String!, $owner: String!) { 
         repository(name: $selected_repo, owner: $owner) {
            id
            object(expression: "master:") {
              ... on Tree {
                commitUrl
                entries {
                  extension
                  name
                  path
                  object {
                    ... on Tree {
                      entries {
                        path
                        name
                        extension
                        object {
                          ... on Tree {
                            id
                            entries {
                              name
                              extension
                              path
                              object {
                                    ... on Blob {
                                      id
                                      text
                                    }
                                  }
                            }
                          }
                          ... on Blob {
                            id
                            text
                          }
                        }
                      }
                    }
                    ... on Blob {
                      id
                      text
                    }
                  }                  
                }
              }
              ... on Blob {
                text
              }
            }
          }
        }
"""