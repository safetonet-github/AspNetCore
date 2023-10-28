import os
import xml.etree.ElementTree as ET

def find_file_in_tree(root, filename):
    for dirpath, dirnames, filenames in os.walk(root):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None

def parse_csproj(file_path, valid_references):
    tree = ET.parse(file_path)
    root = tree.getroot()

    sdk = root.get("Sdk")
    if sdk:
        print(f"File: {file_path} uses SDK: {sdk}")

    references = [
        {
            "id": ref.get('Include').replace("Microsoft", "Jokersoft"),
            "version": "7.0.13"
        }
        for ref in root.findall(".//Reference")
        if ref.get('Include') in valid_references
    ]

    # Create package references in the XML
    item_group = ET.SubElement(root, "ItemGroup")
    for ref in references:
        package_ref = ET.SubElement(item_group, "PackageReference")
        package_ref.set("Include", ref["id"])
        package_ref.set("Version", ref["version"])

    # Set the PackageId for publishing
    package_id = ET.SubElement(root, "PropertyGroup")
    id_elem = ET.SubElement(package_id, "PackageId")
    id_elem.text = os.path.basename(file_path).replace(".csproj", "").replace("Microsoft", "Jokersoft")

    # Beautify the XML
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    formatted_xml = '\n'.join(line for line in xml_str.splitlines() if line.strip())

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(formatted_xml)

    return sdk, references

valid_references  = {
    "Microsoft.AspNetCore.Components.CustomElements",
    "Microsoft.AspNetCore.RateLimiting",
    "Microsoft.AspNetCore.Grpc.Swagger",
    "Microsoft.AspNetCore.Grpc.JsonTranscoding",
    "Microsoft.AspNetCore.RequestDecompression",
    "Microsoft.AspNetCore.OutputCaching",
    "Microsoft.AspNetCore.App.CodeFixes",
    "Microsoft.AspNetCore.App.Analyzers",
    "Microsoft.AspNetCore.SignalR.Client.SourceGenerator",
    "Microsoft.AspNetCore.Http.Results",
    "Microsoft.AspNetCore.HttpLogging",
    "Microsoft.Extensions.Caching.StackExchangeRedis",
    "Microsoft.Extensions.Caching.SqlServer",
    "Microsoft.Extensions.Http.Polly",
    "Microsoft.Web.Xdt.Extensions",
    "Microsoft.Extensions.Localization",
    "Microsoft.Extensions.Configuration.KeyPerFile",
    "Microsoft.AspNetCore.SignalR.StackExchangeRedis",
    "Microsoft.AspNetCore.ConcurrencyLimiter",
    "Microsoft.AspNetCore.HeaderPropagation",
    "Microsoft.AspNetCore.Session",
    "Microsoft.AspNetCore.ResponseCaching",
    "Microsoft.AspNetCore.ResponseCaching.Abstractions",
    "Microsoft.AspNetCore.Localization.Routing",
    "Microsoft.AspNetCore.Localization",
    "Microsoft.Extensions.Localization.Abstractions",
    "Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore",
    "Microsoft.AspNetCore.Diagnostics.HealthChecks",
    "Microsoft.Extensions.Diagnostics.HealthChecks",
    "Microsoft.Extensions.Diagnostics.HealthChecks.Abstractions",
    "Microsoft.AspNetCore.MiddlewareAnalysis",
    "Microsoft.AspNetCore.Rewrite",
    "Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore",
    "Microsoft.AspNetCore.CookiePolicy",
    "Microsoft.AspNetCore.Metadata",
    "Microsoft.AspNetCore.Owin",
    "Microsoft.AspNetCore.Hosting.WindowsServices",
    "Microsoft.AspNetCore.DataProtection.EntityFrameworkCore",
    "Microsoft.AspNetCore.DataProtection.StackExchangeRedis",
    "Microsoft.AspNetCore.Cryptography.KeyDerivation",
    "Microsoft.JSInterop.WebAssembly",
    "Microsoft.AspNetCore.SignalR.Client",
    "Microsoft.AspNetCore.Http.Connections.Client",
    "Microsoft.AspNetCore.SignalR.Client.Core",
    "Microsoft.AspNetCore.JsonPatch",
    "Microsoft.AspNetCore.SignalR.Protocols.NewtonsoftJson",
    "Microsoft.AspNetCore.SignalR.Protocols.MessagePack",
    "Microsoft.AspNetCore.ResponseCompression",
    "Microsoft.AspNetCore",
    "Microsoft.AspNetCore.HttpOverrides",
    "Microsoft.AspNetCore.Server.Kestrel",
    "Microsoft.AspNetCore.Server.Kestrel.Transport.Sockets",
    "Microsoft.AspNetCore.Server.Kestrel.Core",
    "Microsoft.AspNetCore.Hosting",
    "Microsoft.AspNetCore.HostFiltering",
    "Microsoft.AspNetCore.Diagnostics",
    "Microsoft.AspNetCore.Diagnostics.Abstractions",
    "Microsoft.AspNetCore.Components.Performance",
    "Microsoft.AspNetCore.Components.WebAssembly.Server",
    "Microsoft.AspNetCore.Components.Analyzers",
    "Microsoft.AspNetCore.HttpsPolicy",
    "Microsoft.AspNetCore.Analyzers",
    "Microsoft.AspNetCore.Html.Abstractions",
    "Microsoft.AspNetCore.Cors",
    "Microsoft.AspNetCore.Antiforgery",
    "Microsoft.AspNetCore.Components.Server",
    "Microsoft.Extensions.FileProviders.Embedded",
    "Microsoft.Extensions.FileProviders.Embedded.Manifest.Task",
    "Microsoft.AspNetCore.StaticFiles",
    "Microsoft.Extensions.WebEncoders",
    "Microsoft.AspNetCore.SignalR",
    "Microsoft.AspNetCore.Http.Connections",
    "Microsoft.AspNetCore.WebSockets",
    "Microsoft.AspNetCore.Routing",
    "Microsoft.AspNetCore.Routing.Abstractions",
    "Microsoft.AspNetCore.Http.Extensions",
    "Microsoft.AspNetCore.Http",
    "Microsoft.Extensions.ObjectPool",
    "Microsoft.AspNetCore.WebUtilities",
    "Microsoft.AspNetCore.Http.Connections.Common",
    "Microsoft.AspNetCore.Hosting.Abstractions",
    "Microsoft.AspNetCore.Http.Abstractions",
    "Microsoft.AspNetCore.Hosting.Server.Abstractions",
    "Microsoft.AspNetCore.Http.Features",
    "Microsoft.Net.Http.Headers",
    "Microsoft.AspNetCore.SignalR.Core",
    "Microsoft.AspNetCore.SignalR.Protocols.Json",
    "Microsoft.AspNetCore.SignalR.Common",
    "Microsoft.AspNetCore.Connections.Abstractions",
    "Microsoft.Extensions.Features",
    "Microsoft.AspNetCore.DataProtection.Extensions",
    "Microsoft.AspNetCore.DataProtection",
    "Microsoft.AspNetCore.DataProtection.Abstractions",
    "Microsoft.AspNetCore.Cryptography.Internal",
    "Microsoft.AspNetCore.Components.Web",
    "Microsoft.JSInterop",
    "Microsoft.AspNetCore.Components.Forms",
    "Microsoft.AspNetCore.Components",
  }  # Add your filenames here
root_path = "./"  # Replace with your root directory

file_names = [ref + ".csproj" for ref in valid_references]

for file_name in file_names:
    file_path = find_file_in_tree(root_path, file_name)
    if file_path:
        sdk, references = parse_csproj(file_path, valid_references)
