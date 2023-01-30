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
      {
         repository(name: "androidskilltest2", owner: "jelvissilva") {
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