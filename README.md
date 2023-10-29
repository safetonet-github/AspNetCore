[![.NET Foundation](https://img.shields.io/badge/.NET%20Foundation-blueviolet.svg)](https://www.dotnetfoundation.org/)
[![MIT License](https://img.shields.io/github/license/dotnet/aspnetcore?color=%230b0&style=flat-square)](https://github.com/dotnet/aspnetcore/blob/main/LICENSE.txt) [![Help Wanted](https://img.shields.io/github/issues/dotnet/aspnetcore/help%20wanted?color=%232EA043&label=help%20wanted&style=flat-square)](https://github.com/dotnet/aspnetcore/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) [![Good First Issues](https://img.shields.io/github/issues/dotnet/aspnetcore/good%20first%20issue?color=%23512BD4&label=good%20first%20issue&style=flat-square)](https://github.com/dotnet/aspnetcore/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
[![Discord](https://img.shields.io/discord/732297728826277939?style=flat-square&label=Discord&logo=discord&logoColor=white&color=7289DA)](https://aka.ms/dotnet-discord)

This Is A Giant Hack
====================

I wanted Kestrel and other core ASP.NET functionality to work on all platforms, including MAUI supported platforms. Ever since about version 2.2.*, Microsoft moved these things from independent packages to forcing users to pull in the entire Web SDK to use them. I hacked and slashed through AspNetCore until I could get a bunch of packages compiling independently. YMMV and use at your own risk. To summarize changes:

I changed the package names only. The project does generate some namespaces but AFAIK, they're all internal. In other words, there are some cases where code is in Jokersoft.* NS, but should only be internal. Therefore, should be a drop-in replacement with original MS namespaces preserved. You will therefore get conflicts if you import both the Jokersoft.* package and matching real Microsoft.* package.

Some caveats:

- Not every single package was published. There will be some missing. There are 90 published by my count. Razor, MVC etc dropped IIRC.
- No guarantees that they all work. I have no time to test 90 packages on every platform.
- I deleted / excluded the authorization packages and there is strong coupling in Kestrel and SignalR to them. I placed throw NotImplementedException in some of function calls that are coupled, and outright deleted the authorization middleware integration in kestrel core. So, you'd need to bring in your own auth middleware and make sure it takes priority over other middlware. THIS HAS BIG SECURITY IMPLICATIONS SO CONSIDER THIS WISELY.
- I can live with these shortcomings cause I just need a high performance HTTP server for proxying. It's probably the best that can be done while we wait to see what Microsoft will do to sort out their cross-platform plan.

This is a hack / mess and the only benefit to publishing this is for people to repro packages on their own and for transparency/security.

Thise code is based on the [tagged release 7.0.13](https://github.com/dotnet/aspnetcore/tree/v7.0.13).

These packages are [available on Nuget](https://www.nuget.org/packages?q=jokersoft).

***

ASP.NET Core
============

ASP.NET Core is an open-source and cross-platform framework for building modern cloud based internet connected applications, such as web apps, IoT apps and mobile backends. ASP.NET Core apps run on [.NET](https://dot.net), a free, cross-platform and open-source application runtime. It was architected to provide an optimized development framework for apps that are deployed to the cloud or run on-premises. It consists of modular components with minimal overhead, so you retain flexibility while constructing your solutions. You can develop and run your ASP.NET Core apps cross-platform on Windows, Mac and Linux. [Learn more about ASP.NET Core](https://docs.microsoft.com/aspnet/core/).

## Get Started

Follow the [Getting Started](https://docs.microsoft.com/aspnet/core/getting-started) instructions in the [ASP.NET Core docs](https://docs.microsoft.com/aspnet/index).

Also check out the [.NET Homepage](https://www.microsoft.com/net) for released versions of .NET, getting started guides, and learning resources.

See the [Triage Process](https://github.com/dotnet/aspnetcore/blob/main/docs/TriageProcess.md) document for more information on how we handle incoming issues.

## How to Engage, Contribute, and Give Feedback

Some of the best ways to contribute are to try things out, file issues, join in design conversations,
and make pull-requests.

* [Download our latest daily builds](./docs/DailyBuilds.md)
* Follow along with the development of ASP.NET Core:
    * [Community Standup](https://live.asp.net): The community standup is held every week and streamed live to YouTube. You can view past standups in the linked playlist.
    * [Roadmap](https://aka.ms/aspnet/roadmap): The schedule and milestone themes for ASP.NET Core.
* [Build ASP.NET Core source code](./docs/BuildFromSource.md)
* Check out the [contributing](CONTRIBUTING.md) page to see the best places to log issues and start discussions.

## Reporting security issues and bugs

Security issues and bugs should be reported privately, via email, to the Microsoft Security Response Center (MSRC)  secure@microsoft.com. You should receive a response within 24 hours. If for some reason you do not, please follow up via email to ensure we received your original message. Further information, including the MSRC PGP key, can be found in the [Security TechCenter](https://technet.microsoft.com/en-us/security/ff852094.aspx).

## Related projects

These are some other repos for related projects:

* [Documentation](https://github.com/aspnet/Docs) - documentation sources for https://docs.microsoft.com/aspnet/core/
* [Entity Framework Core](https://github.com/dotnet/efcore) - data access technology
* [Runtime](https://github.com/dotnet/runtime) - cross-platform runtime for cloud, mobile, desktop, and IoT apps
* [Razor Compiler](https://github.com/dotnet/razor-compiler) - the parser and the C# code generator for the Razor syntax
* [Razor Tooling](https://github.com/dotnet/razor-tooling) - tools for working on Razor ASP.NET Core apps using [Visual Studio](https://visualstudio.com), [Visual Studio for Mac](https://visualstudio.microsoft.com/vs/mac/), and [Visual Studio Code](https://code.visualstudio.com/).

## Code of conduct

See [CODE-OF-CONDUCT](./CODE-OF-CONDUCT.md)
