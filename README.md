&nbsp;

<div align="center">

<img src="https://raw.githubusercontent.com/AgnostiqHQ/covalent/master/doc/source/_static/covalent_readme_banner.svg" width=150%>

[![covalent](https://img.shields.io/badge/covalent-0.177.0-purple)](https://github.com/AgnostiqHQ/covalent)
[![agpl](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html)

</div>

## Covalent AWS Plugins

<img src="./doc/static/covalent-ec2-code-example.png" width="400px" align="right">

Covalent is a python based workflow orchestration tool used to execute HPC and quantum tasks in heterogenous environments.

By installing Covalent AWS Plugins users can leverage a broad plugin ecosystem to execute tasks using AWS resources best fit for each task.

Covalent AWS Plugins installs a set of executor plugins that allow tasks to be run in an EC2 instance, AWS Lambda, AWS ECS Cluster, AWS Batch Compute Environment, and as an AWS Braket Job for tasks requiring Quantum devices.

## Installation


To use this plugin with Covalent, simply install it with `pip`:

```bash
pip install covalent-aws-plugins
```


## Included Plugins

While each plugin can be seperately installed installing the above pip package installs all of the below plugins.

| | Plugin Name | Use Case | Example Usage |
|---|-------------|-------------|---|
|<svg class="w-6 h-6" height="40" width="40" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient x1="0%" y1="100%" x2="100%" y2="0%" id="Arch_AWS-Batch_32_svg__a"><stop stop-color="#C8511B" offset="0%"></stop><stop stop-color="#F90" offset="100%"></stop></linearGradient></defs><g fill="none" fill-rule="evenodd"><path d="M0 0h40v40H0z" fill="url(#Arch_AWS-Batch_32_svg__a)"></path><path d="M20.568 29.523c.607 0 1.098.489 1.098 1.092 0 .603-.491 1.093-1.098 1.093-.606 0-1.098-.49-1.098-1.093s.492-1.092 1.098-1.092m-9.004-9.047c0 .604-.493 1.093-1.1 1.093a1.095 1.095 0 01-1.097-1.093c0-.602.491-1.092 1.098-1.092.606 0 1.099.49 1.099 1.092M30.748 32.93c-1.255 0-2.239-.943-2.239-2.146a2.236 2.236 0 012.24-2.228c1.235 0 2.24 1 2.24 2.228 0 1.203-.984 2.146-2.24 2.146m-2.24-12.398a2.236 2.236 0 012.24-2.228c1.235 0 2.24 1 2.24 2.228a2.236 2.236 0 01-2.24 2.227c-1.235 0-2.24-1-2.24-2.227m-7.94 2.23c-1.236 0-2.241-1-2.241-2.228a2.237 2.237 0 012.24-2.228c1.236 0 2.24 1 2.24 2.228a2.237 2.237 0 01-2.24 2.228m2.454 7.792c0 1.391-1.054 2.44-2.454 2.44-1.399 0-2.454-1.049-2.454-2.44 0-1.392 1.055-2.44 2.454-2.44 1.4 0 2.454 1.048 2.454 2.44m-5.401-19.619c0-1.533 1.405-2.93 2.947-2.93s2.947 1.397 2.947 2.93c0 1.534-1.405 2.93-2.947 2.93s-2.947-1.396-2.947-2.93m-7.156 12.041c-1.4 0-2.454-1.048-2.454-2.44 0-1.412 1.101-2.561 2.454-2.561 1.354 0 2.455 1.149 2.455 2.561 0 1.392-1.056 2.44-2.455 2.44m2.233 7.795c0 1.213-.985 2.164-2.24 2.164-1.257 0-2.242-.95-2.242-2.164a2.237 2.237 0 012.242-2.228c1.235 0 2.24 1 2.24 2.228m18.556-3.17v-3.887C32.806 23.471 34 22.144 34 20.533c0-1.783-1.458-3.233-3.252-3.233a3.243 3.243 0 00-3.2 2.733h-3.78a3.231 3.231 0 00-2.694-2.68v-2.535c1.888-.266 3.452-1.956 3.452-3.882C24.526 8.84 22.677 7 20.568 7s-3.958 1.84-3.958 3.936c0 1.926 1.564 3.616 3.453 3.882v2.535a3.231 3.231 0 00-2.695 2.68h-3.487c-.241-1.727-1.674-3.063-3.416-3.063C8.554 16.97 7 18.57 7 20.537c0 1.76 1.267 3.158 2.96 3.396v3.656c-1.556.24-2.755 1.57-2.755 3.183 0 1.777 1.429 3.17 3.253 3.17s3.251-1.393 3.251-3.17c0-1.609-1.19-2.935-2.739-3.181v-3.658a3.384 3.384 0 002.911-2.895h3.487a3.231 3.231 0 002.695 2.68v3.44c-1.693.239-2.96 1.637-2.96 3.397 0 1.932 1.522 3.445 3.465 3.445 1.943 0 3.465-1.513 3.465-3.445 0-1.76-1.267-3.158-2.96-3.397v-3.44a3.231 3.231 0 002.695-2.68h3.78a3.234 3.234 0 002.695 2.677v3.887c-1.552.244-2.745 1.572-2.745 3.183 0 1.767 1.428 3.152 3.25 3.152 1.824 0 3.252-1.385 3.252-3.152 0-1.61-1.194-2.939-2.746-3.183" fill="#FFF"></path></g></svg>| AWS Batch Executor |**Useful for heavy compute workloads (high CPU/memory).** Tasks are queued to execute in the user defined Batch compute environment.| [Example](https://covalent.readthedocs.io/en/latest/api/executors/awsbatch.html#usage-example)|
|<svg class="w-6 h-6" height="40" width="40" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient x1="0%" y1="100%" x2="100%" y2="0%" id="Arch_Amazon-EC2_32_svg__a"><stop stop-color="#C8511B" offset="0%"></stop><stop stop-color="#F90" offset="100%"></stop></linearGradient></defs><g fill="none" fill-rule="evenodd"><path d="M0 0h40v40H0z" fill="url(#Arch_Amazon-EC2_32_svg__a)"></path><path d="M26.052 27L26 13.948 13 14v13.052L26.052 27zM27 14h2v1h-2v2h2v1h-2v2h2v1h-2v2h2v1h-2v2h2v1h-2v.052a.95.95 0 01-.948.948H26v2h-1v-2h-2v2h-1v-2h-2v2h-1v-2h-2v2h-1v-2h-2v2h-1v-2h-.052a.95.95 0 01-.948-.948V27h-2v-1h2v-2h-2v-1h2v-2h-2v-1h2v-2h-2v-1h2v-2h-2v-1h2v-.052a.95.95 0 01.948-.948H13v-2h1v2h2v-2h1v2h2v-2h1v2h2v-2h1v2h2v-2h1v2h.052a.95.95 0 01.948.948V14zm-6 19H7V19h2v-1H7.062C6.477 18 6 18.477 6 19.062v13.876C6 33.523 6.477 34 7.062 34h13.877c.585 0 1.061-.477 1.061-1.062V31h-1v2zM34 7.062v13.876c0 .585-.476 1.062-1.061 1.062H30v-1h3V7H19v3h-1V7.062C18 6.477 18.477 6 19.062 6h13.877C33.524 6 34 6.477 34 7.062z" fill="#FFF"></path></g></svg>|AWS EC2 Executor|**General purpose compute workloads users can select compute resources.** An EC2 instance is auto-provisioned using terraform with selected compute settings to execute workflow tasks.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awsec2.html#usage-example)|
|<svg class="w-6 h-6" height="40" width="40" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient x1="0%" y1="100%" x2="100%" y2="0%" id="Arch_AWS-Braket_32_svg__a"><stop stop-color="#C8511B" offset="0%"></stop><stop stop-color="#F90" offset="100%"></stop></linearGradient></defs><g fill="none" fill-rule="evenodd"><path d="M0 0h40v40H0z" fill="url(#Arch_AWS-Braket_32_svg__a)"></path><path d="M20.965 23.463c0 .827.673 1.5 1.5 1.5s1.5-.673 1.5-1.5-.673-1.5-1.5-1.5-1.5.673-1.5 1.5zm.29 2.175c-4.854 4.474-10.314 8.29-13.245 8.29-.613 0-1.116-.167-1.48-.53-1.24-1.238-.106-3.976 1.36-6.435h1.182c-2.12 3.4-2.346 5.216-1.835 5.728 1.137 1.137 6.499-1.503 13.254-7.711a2.476 2.476 0 01-.526-1.517c0-1.378 1.12-2.5 2.5-2.5.59 0 1.125.213 1.553.556 6.62-6.938 9.89-13.067 8.675-14.284-.51-.505-2.321-.29-5.728 1.835V7.888c2.428-1.447 5.189-2.603 6.435-1.36 2.143 2.143-2.742 9.5-8.74 15.766.189.35.305.745.305 1.169 0 1.378-1.121 2.5-2.5 2.5-.44 0-.85-.125-1.21-.325zm7.71-5.9v9.225H19.74c-.597.5-1.19.983-1.776 1.437v2.563h1v-3h2v3h1v-3h2v3h1v-3h2v3h1v-3h1.5a.5.5 0 00.5-.5v-1.5h3v-1h-3v-2h3v-1h-3v-2h3v-1h-3v-2h3v-1h-2.563a63.408 63.408 0 01-1.437 1.776zm-19 5.225h-3v-1h3v-2h-3v-1h3v-2h-3v-1h3v-2h-3v-1h3v-2h-3v-1h3v-1.5a.5.5 0 01.5-.5h1.5v-3h1v3h2v-3h1v3h2v-3h1v3h2v-3h1v3h2v-3h1v3h4.5a.5.5 0 01.5.5v1.098a31.818 31.818 0 01-1 1.578v-2.176h-18v18h2.177c-.564.379-1.091.712-1.578 1h-1.1a.5.5 0 01-.5-.5v-4.5z" fill="#FFF"></path></g></svg>|AWS Braket Executor|**Suitable for Quantum/Classical hybrid workflows.** Tasks are executed using a combination of classical and quantum devices.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awsbraket.html#usage-example)|
|<svg class="w-6 h-6" height="40" width="40" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient x1="0%" y1="100%" x2="100%" y2="0%" id="Arch_Amazon-Elastic-Container-Service_32_svg__a"><stop stop-color="#C8511B" offset="0%"></stop><stop stop-color="#F90" offset="100%"></stop></linearGradient></defs><g fill="none" fill-rule="evenodd"><path d="M0 0h40v40H0z" fill="url(#Arch_Amazon-Elastic-Container-Service_32_svg__a)"></path><path d="M32 24.25l-4-2.357v-6.068a.492.492 0 00-.287-.444L22 12.736V8.285l10 4.897V24.25zm.722-11.811l-11-5.387a.504.504 0 00-.485.022.49.49 0 00-.237.417v5.557c0 .19.111.363.287.444L27 16.136v6.035c0 .172.091.332.243.42l5 2.947a.501.501 0 00.757-.42v-12.24a.49.49 0 00-.278-.44zM19.995 32.952L9 27.317V13.169l9-4.849v4.442l-4.746 2.636a.488.488 0 00-.254.427v8.842a.49.49 0 00.258.43l6.5 3.515a.508.508 0 00.482.001l6.25-3.371 3.546 2.33-10.041 5.38zm6.799-8.693a.51.51 0 00-.519-.022L20 27.622l-6-3.245v-8.265l4.746-2.637a.489.489 0 00.254-.427V7.49a.489.489 0 00-.245-.422.512.512 0 00-.496-.01l-10 5.388a.49.49 0 00-.259.43v14.737c0 .184.103.35.268.436l11.5 5.895a.52.52 0 00.471-.005l11-5.895a.486.486 0 00.039-.839l-4.484-2.947z" fill="#FFF"></path></g></svg>|AWS ECS Executor|**Useful for moderate to heavy workloads (low memory requirements).** Covalent tasks are executed in containers within an AWS ECS cluster.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awsecs.html#usage-example)|
|<svg class="w-6 h-6" height="40" width="40" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient x1="0%" y1="100%" x2="100%" y2="0%" id="Arch_AWS-Lambda_32_svg__a"><stop stop-color="#C8511B" offset="0%"></stop><stop stop-color="#F90" offset="100%"></stop></linearGradient></defs><g fill="none" fill-rule="evenodd"><path d="M0 0h40v40H0z" fill="url(#Arch_AWS-Lambda_32_svg__a)"></path><path d="M14.386 33H8.27l6.763-14.426 3.064 6.44L14.387 33zm1.085-15.798a.49.49 0 00-.442-.282h-.002a.493.493 0 00-.441.285l-7.538 16.08a.507.507 0 00.028.482c.09.145.247.233.415.233h7.206c.19 0 .363-.111.445-.286l3.944-8.489a.508.508 0 00-.002-.432l-3.613-7.591zM32.018 33h-5.882l-9.47-20.711a.491.491 0 00-.444-.289H12.37l.005-5h7.549l9.424 20.71c.08.177.256.29.446.29h2.224v5zm.49-6h-2.4L20.684 6.29a.492.492 0 00-.446-.29h-8.353a.496.496 0 00-.491.5l-.006 6c0 .132.052.259.144.354a.488.488 0 00.347.146h4.032l9.468 20.711c.08.176.254.289.445.289h6.686a.495.495 0 00.491-.5v-6c0-.276-.219-.5-.491-.5z" fill="#FFF"></path></g></svg>|AWS Lambda Executor|**Suitable for short lived tasks that can be parallalized.** Tasks are executed in a AWS Lambda.|[Example](https://covalent.readthedocs.io/en/latest/api/executors/awslambda.html#usage-example)|



## Release Notes

Release notes are available in the [Changelog](https://github.com/AgnostiqHQ/covalent-aws-plugins/blob/main/CHANGELOG.md).

## Citation

Please use the following citation in any publications:

> W. J. Cunningham, S. K. Radha, F. Hasan, J. Kanem, S. W. Neagle, and S. Sanand.
> *Covalent.* Zenodo, 2022. https://doi.org/10.5281/zenodo.5903364

## License

Covalent is licensed under the GNU Affero GPL 3.0 License. Covalent may be distributed under other licenses upon request. See the [LICENSE](https://github.com/AgnostiqHQ/covalent-braket-plugin/blob/main/LICENSE) file or contact the [support team](mailto:support@agnostiq.ai) for more details.
