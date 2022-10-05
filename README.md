&nbsp;

<div align="center">

<img src="https://raw.githubusercontent.com/AgnostiqHQ/covalent/master/doc/source/_static/covalent_readme_banner.svg" width=150%>

[![covalent](https://img.shields.io/badge/covalent-0.177.0-purple)](https://github.com/AgnostiqHQ/covalent)
[![agpl](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html)

</div>

## Covalent AWS Plugins

<img src="./doc/static/covalent-ec2-code-example.png" width="550px" align="right">

[Covalent](https://github.com/AgnostiqHQ/covalent) is a python based workflow orchestration tool used to execute HPC and quantum tasks in heterogenous environments.

By installing Covalent AWS Plugins users can leverage a broad plugin ecosystem to execute tasks using AWS resources best fit for each task.

Covalent AWS Plugins installs a set of executor plugins that allow tasks to be run in an EC2 instance, AWS Lambda, AWS ECS Cluster, AWS Batch Compute Environment, and as an AWS Braket Job for tasks requiring Quantum devices.

If you're new to covalent see visit our [Getting Started Guide](https://covalent.readthedocs.io/en/latest/getting_started/index.html).



## Installation


To use this plugin with Covalent, simply install it with `pip`:

```bash
pip install covalent-aws-plugins
```

> You may require [Docker](https://docs.docker.com/get-docker/) for Braket and [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) to be installed to use the Braket & EC2 plugins respectively.

## Included Plugins

While each plugin can be seperately installed installing the above pip package installs all of the below plugins.

| | Plugin Name | Use Case | Example Usage |
|---|-------------|-------------|---|
|![AWS Batch](./doc/static/Batch.png)| AWS Batch Executor |**Useful for heavy compute workloads (high CPU/memory).** Tasks are queued to execute in the user defined Batch compute environment.| [Example](https://covalent.readthedocs.io/en/latest/api/executors/awsbatch.html#usage-example)|
|![AWS EC2](./doc/static/EC2.png)|AWS EC2 Executor|**General purpose compute workloads users can select compute resources.** An EC2 instance is auto-provisioned using terraform with selected compute settings to execute workflow tasks.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awsec2.html#usage-example)|
|![AWS EC2](./doc/static/Braket.png)|AWS Braket Executor|**Suitable for Quantum/Classical hybrid workflows.** Tasks are executed using a combination of classical and quantum devices.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awsbraket.html#usage-example)|
|![AWS EC2](./doc/static/ECS.png)|AWS ECS Executor|**Useful for moderate to heavy workloads (low memory requirements).** Covalent tasks are executed in containers within an AWS ECS cluster.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awsecs.html#usage-example)|
|![AWS EC2](./doc/static/Lambda.png)|AWS Lambda Executor|**Suitable for short lived tasks that can be parallalized.** Tasks are executed in a AWS Lambda.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awslambda.html#usage-example)|



## Release Notes

Release notes are available in the [Changelog](https://github.com/AgnostiqHQ/covalent-aws-plugins/blob/main/CHANGELOG.md).

## Citation

Please use the following citation in any publications:

> W. J. Cunningham, S. K. Radha, F. Hasan, J. Kanem, S. W. Neagle, and S. Sanand.
> *Covalent.* Zenodo, 2022. https://doi.org/10.5281/zenodo.5903364

## License

Covalent is licensed under the GNU Affero GPL 3.0 License. Covalent may be distributed under other licenses upon request. See the [LICENSE](https://github.com/AgnostiqHQ/covalent-braket-plugin/blob/main/LICENSE) file or contact the [support team](mailto:support@agnostiq.ai) for more details.
