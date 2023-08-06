## Publishing to PyPI from GitLab CI

I will briefly note down the steps:

1. Ensure that you create protected tags for versions (See Settings/Repository/Protected Tags)
    - This is required because the variables created in step 2 is protected and can only be
      accessed from a protected branch ([link](https://github.com/pypa/twine/issues/461))
2. Create API token for project in PyPI and add the below variables under Settings/CI-CD/Variables
    - TWINE\_USERNAME: \_\_token\_\_
    - TWINE\_PASSWORD: pypi-(secret API token)

And voila, with the given [.gitlab-ci.yml](.gitlab-ci.yml) file, the release
pipeline should be triggered for every **protected** version tag (like v0.0.2)
created in gitlab repository. Note that the pipeline will succed only if the tag
is protected.

The version tag can be created in gitlab repo directly rather than locally and then pushing.
This has the added advantage of being paired with a GitLab release easily.