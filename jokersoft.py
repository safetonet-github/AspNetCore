import os
import xml.etree.ElementTree as ET

def update_sln_file(sln_file_path, valid_references):
    # Read the SLN file
    with open(sln_file_path, 'r', encoding="utf-8") as file:
        content = file.read()

    # Perform the replacements
    for ref in valid_references:
        jokersoft_ref = ref.replace("Microsoft.", "Jokersoft.")
        proj_ref = ref.replace("\"", "") + ".csproj"
        joker_proj_ref =  ref.replace("Microsoft.", "Jokersoft.")
        content = content.replace(ref, jokersoft_ref)
        content = content.replace(proj_ref, joker_proj_ref)

    # Print the changed content
    print(content)

    # Uncomment below to save changes
    with open(sln_file_path, 'w', encoding="utf-8") as file:
        file.write(content)

valid_references = [
    "\"Microsoft.AspNetCore.Components.CustomElements\"",
    "\"Microsoft.AspNetCore.RateLimiting\"",
    "\"Microsoft.AspNetCore.Grpc.Swagger\"",
    "\"Microsoft.AspNetCore.Grpc.JsonTranscoding\"",
    "\"Microsoft.AspNetCore.RequestDecompression\"",
    "\"Microsoft.AspNetCore.OutputCaching\"",
    "\"Microsoft.AspNetCore.App.CodeFixes\"",
    "\"Microsoft.AspNetCore.App.Analyzers\"",
    "\"Microsoft.AspNetCore.SignalR.Client.SourceGenerator\"",
    "\"Microsoft.AspNetCore.Http.Results\"",
    "\"Microsoft.AspNetCore.HttpLogging\"",
    "\"Microsoft.Extensions.Caching.StackExchangeRedis\"",
    "\"Microsoft.Extensions.Caching.SqlServer\"",
    "\"Microsoft.Extensions.Http.Polly\"",
    "\"Microsoft.Web.Xdt.Extensions\"",
    "\"Microsoft.Extensions.Localization\"",
    "\"Microsoft.Extensions.Configuration.KeyPerFile\"",
    "\"Microsoft.AspNetCore.SignalR.StackExchangeRedis\"",
    "\"Microsoft.AspNetCore.ConcurrencyLimiter\"",
    "\"Microsoft.AspNetCore.HeaderPropagation\"",
    "\"Microsoft.AspNetCore.Session\"",
    "\"Microsoft.AspNetCore.ResponseCaching\"",
    "\"Microsoft.AspNetCore.ResponseCaching.Abstractions\"",
    "\"Microsoft.AspNetCore.Localization.Routing\"",
    "\"Microsoft.AspNetCore.Localization\"",
    "\"Microsoft.Extensions.Localization.Abstractions\"",
    "\"Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore\"",
    "\"Microsoft.AspNetCore.Diagnostics.HealthChecks\"",
    "\"Microsoft.Extensions.Diagnostics.HealthChecks\"",
    "\"Microsoft.Extensions.Diagnostics.HealthChecks.Abstractions\"",
    "\"Microsoft.AspNetCore.MiddlewareAnalysis\"",
    "\"Microsoft.AspNetCore.Rewrite\"",
    "\"Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore\"",
    "\"Microsoft.AspNetCore.CookiePolicy\"",
    "\"Microsoft.AspNetCore.Metadata\"",
    "\"Microsoft.AspNetCore.Owin\"",
    "\"Microsoft.AspNetCore.Hosting.WindowsServices\"",
    "\"Microsoft.AspNetCore.DataProtection.EntityFrameworkCore\"",
    "\"Microsoft.AspNetCore.DataProtection.StackExchangeRedis\"",
    "\"Microsoft.AspNetCore.Cryptography.KeyDerivation\"",
    "\"Microsoft.JSInterop.WebAssembly\"",
    "\"Microsoft.AspNetCore.SignalR.Client\"",
    "\"Microsoft.AspNetCore.Http.Connections.Client\"",
    "\"Microsoft.AspNetCore.SignalR.Client.Core\"",
    "\"Microsoft.AspNetCore.JsonPatch\"",
    "\"Microsoft.AspNetCore.SignalR.Protocols.NewtonsoftJson\"",
    "\"Microsoft.AspNetCore.SignalR.Protocols.MessagePack\"",
    "\"Microsoft.AspNetCore.ResponseCompression\"",
    "\"Microsoft.AspNetCore\"",
    "\"Microsoft.AspNetCore.HttpOverrides\"",
    "\"Microsoft.AspNetCore.Server.Kestrel\"",
    "\"Microsoft.AspNetCore.Server.Kestrel.Transport.Sockets\"",
    "\"Microsoft.AspNetCore.Server.Kestrel.Core\"",
    "\"Microsoft.AspNetCore.Hosting\"",
    "\"Microsoft.AspNetCore.HostFiltering\"",
    "\"Microsoft.AspNetCore.Diagnostics\"",
    "\"Microsoft.AspNetCore.Diagnostics.Abstractions\"",
    "\"Microsoft.AspNetCore.Components.Performance\"",
    "\"Microsoft.AspNetCore.Components.WebAssembly.Server\"",
    "\"Microsoft.AspNetCore.Components.Analyzers\"",
    "\"Microsoft.AspNetCore.HttpsPolicy\"",
    "\"Microsoft.AspNetCore.Analyzers\"",
    "\"Microsoft.AspNetCore.Html.Abstractions\"",
    "\"Microsoft.AspNetCore.Cors\"",
    "\"Microsoft.AspNetCore.Antiforgery\"",
    "\"Microsoft.AspNetCore.Components.Server\"",
    "\"Microsoft.Extensions.FileProviders.Embedded\"",
    "\"Microsoft.Extensions.FileProviders.Embedded.Manifest.Task\"",
    "\"Microsoft.AspNetCore.StaticFiles\"",
    "\"Microsoft.Extensions.WebEncoders\"",
    "\"Microsoft.AspNetCore.SignalR\"",
    "\"Microsoft.AspNetCore.Http.Connections\"",
    "\"Microsoft.AspNetCore.WebSockets\"",
    "\"Microsoft.AspNetCore.Routing\"",
    "\"Microsoft.AspNetCore.Routing.Abstractions\"",
    "\"Microsoft.AspNetCore.Http.Extensions\"",
    "\"Microsoft.AspNetCore.Http\"",
    "\"Microsoft.Extensions.ObjectPool\"",
    "\"Microsoft.AspNetCore.WebUtilities\"",
    "\"Microsoft.AspNetCore.Http.Connections.Common\"",
    "\"Microsoft.AspNetCore.Hosting.Abstractions\"",
    "\"Microsoft.AspNetCore.Http.Abstractions\"",
    "\"Microsoft.AspNetCore.Hosting.Server.Abstractions\"",
    "\"Microsoft.AspNetCore.Http.Features\"",
    "\"Microsoft.Net.Http.Headers\"",
    "\"Microsoft.AspNetCore.SignalR.Core\"",
    "\"Microsoft.AspNetCore.SignalR.Protocols.Json\"",
    "\"Microsoft.AspNetCore.SignalR.Common\"",
    "\"Microsoft.AspNetCore.Connections.Abstractions\"",
    "\"Microsoft.Extensions.Features\"",
    "\"Microsoft.AspNetCore.DataProtection.Extensions\"",
    "\"Microsoft.AspNetCore.DataProtection\"",
    "\"Microsoft.AspNetCore.DataProtection.Abstractions\"",
    "\"Microsoft.AspNetCore.Cryptography.Internal\"",
    "\"Microsoft.AspNetCore.Components.Web\"",
    "\"Microsoft.JSInterop\"",
    "\"Microsoft.AspNetCore.Components.Forms\"",
    "\"Microsoft.AspNetCore.Components\"",
]

sln_file_path = "./eng/TrimmableProjects.props"  # Replace with the path to your .sln file
update_sln_file(sln_file_path, valid_references)

exit()

def find_file_in_tree(root, filename):
    for dirpath, dirnames, filenames in os.walk(root):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    return None

def rename_file(file_path, new_name):
    directory = os.path.dirname(file_path)
    new_path = os.path.join(directory, new_name)
    os.rename(file_path, new_path)
    return new_path

def process_csproj(file_path, valid_references):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Print the SDK
    sdk = root.get("Sdk")
    if sdk:
        print(f"File: {file_path} uses SDK: {sdk}")

    # Replace matching text with "Jokersoft" version
    for ref in valid_references:
        jokersoft_ref = ref.replace("Microsoft\"", "Jokersoft")
        for elem in root.iter():
            if elem.text and ref in elem.text:
                elem.text = elem.text.replace(ref, jokersoft_ref)
            for key, value in elem.attrib.items():
                if ref in value:
                    elem.attrib[key] = value.replace(ref, jokersoft_ref)

    # Add GeneratePackageOnBuild if not present
    prop_group = root.find(".//PropertyGroup")
    if not root.find(".//GeneratePackageOnBuild"):
        gen_package = ET.SubElement(prop_group, "GeneratePackageOnBuild")
        gen_package.text = "True"

    # Print the modified XML content
    xml_str = ET.tostring(root, encoding="unicode\"", method="xml")
    formatted_xml = '\n'.join(line for line in xml_str.splitlines() if line.strip())
    print("\nModified Content for:\"", file_path)
    print(formatted_xml)
    print("\n" + "-"*80 + "\n")

    # Uncomment below to save
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(formatted_xml)

valid_references  = {
    "\"Microsoft.AspNetCore.Components.CustomElements\"",
    "\"Microsoft.AspNetCore.RateLimiting\"",
    "\"Microsoft.AspNetCore.Grpc.Swagger\"",
    "\"Microsoft.AspNetCore.Grpc.JsonTranscoding\"",
    "\"Microsoft.AspNetCore.RequestDecompression\"",
    "\"Microsoft.AspNetCore.OutputCaching\"",
    "\"Microsoft.AspNetCore.App.CodeFixes\"",
    "\"Microsoft.AspNetCore.App.Analyzers\"",
    "\"Microsoft.AspNetCore.SignalR.Client.SourceGenerator\"",
    "\"Microsoft.AspNetCore.Http.Results\"",
    "\"Microsoft.AspNetCore.HttpLogging\"",
    "\"Microsoft.Extensions.Caching.StackExchangeRedis\"",
    "\"Microsoft.Extensions.Caching.SqlServer\"",
    "\"Microsoft.Extensions.Http.Polly\"",
    "\"Microsoft.Web.Xdt.Extensions\"",
    "\"Microsoft.Extensions.Localization\"",
    "\"Microsoft.Extensions.Configuration.KeyPerFile\"",
    "\"Microsoft.AspNetCore.SignalR.StackExchangeRedis\"",
    "\"Microsoft.AspNetCore.ConcurrencyLimiter\"",
    "\"Microsoft.AspNetCore.HeaderPropagation\"",
    "\"Microsoft.AspNetCore.Session\"",
    "\"Microsoft.AspNetCore.ResponseCaching\"",
    "\"Microsoft.AspNetCore.ResponseCaching.Abstractions\"",
    "\"Microsoft.AspNetCore.Localization.Routing\"",
    "\"Microsoft.AspNetCore.Localization\"",
    "\"Microsoft.Extensions.Localization.Abstractions\"",
    "\"Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore\"",
    "\"Microsoft.AspNetCore.Diagnostics.HealthChecks\"",
    "\"Microsoft.Extensions.Diagnostics.HealthChecks\"",
    "\"Microsoft.Extensions.Diagnostics.HealthChecks.Abstractions\"",
    "\"Microsoft.AspNetCore.MiddlewareAnalysis\"",
    "\"Microsoft.AspNetCore.Rewrite\"",
    "\"Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore\"",
    "\"Microsoft.AspNetCore.CookiePolicy\"",
    "\"Microsoft.AspNetCore.Metadata\"",
    "\"Microsoft.AspNetCore.Owin\"",
    "\"Microsoft.AspNetCore.Hosting.WindowsServices\"",
    "\"Microsoft.AspNetCore.DataProtection.EntityFrameworkCore\"",
    "\"Microsoft.AspNetCore.DataProtection.StackExchangeRedis\"",
    "\"Microsoft.AspNetCore.Cryptography.KeyDerivation\"",
    "\"Microsoft.JSInterop.WebAssembly\"",
    "\"Microsoft.AspNetCore.SignalR.Client\"",
    "\"Microsoft.AspNetCore.Http.Connections.Client\"",
    "\"Microsoft.AspNetCore.SignalR.Client.Core\"",
    "\"Microsoft.AspNetCore.JsonPatch\"",
    "\"Microsoft.AspNetCore.SignalR.Protocols.NewtonsoftJson\"",
    "\"Microsoft.AspNetCore.SignalR.Protocols.MessagePack\"",
    "\"Microsoft.AspNetCore.ResponseCompression\"",
    "\"Microsoft.AspNetCore\"",
    "\"Microsoft.AspNetCore.HttpOverrides\"",
    "\"Microsoft.AspNetCore.Server.Kestrel\"",
    "\"Microsoft.AspNetCore.Server.Kestrel.Transport.Sockets\"",
    "\"Microsoft.AspNetCore.Server.Kestrel.Core\"",
    "\"Microsoft.AspNetCore.Hosting\"",
    "\"Microsoft.AspNetCore.HostFiltering\"",
    "\"Microsoft.AspNetCore.Diagnostics\"",
    "\"Microsoft.AspNetCore.Diagnostics.Abstractions\"",
    "\"Microsoft.AspNetCore.Components.Performance\"",
    "\"Microsoft.AspNetCore.Components.WebAssembly.Server\"",
    "\"Microsoft.AspNetCore.Components.Analyzers\"",
    "\"Microsoft.AspNetCore.HttpsPolicy\"",
    "\"Microsoft.AspNetCore.Analyzers\"",
    "\"Microsoft.AspNetCore.Html.Abstractions\"",
    "\"Microsoft.AspNetCore.Cors\"",
    "\"Microsoft.AspNetCore.Antiforgery\"",
    "\"Microsoft.AspNetCore.Components.Server\"",
    "\"Microsoft.Extensions.FileProviders.Embedded\"",
    "\"Microsoft.Extensions.FileProviders.Embedded.Manifest.Task\"",
    "\"Microsoft.AspNetCore.StaticFiles\"",
    "\"Microsoft.Extensions.WebEncoders\"",
    "\"Microsoft.AspNetCore.SignalR\"",
    "\"Microsoft.AspNetCore.Http.Connections\"",
    "\"Microsoft.AspNetCore.WebSockets\"",
    "\"Microsoft.AspNetCore.Routing\"",
    "\"Microsoft.AspNetCore.Routing.Abstractions\"",
    "\"Microsoft.AspNetCore.Http.Extensions\"",
    "\"Microsoft.AspNetCore.Http\"",
    "\"Microsoft.Extensions.ObjectPool\"",
    "\"Microsoft.AspNetCore.WebUtilities\"",
    "\"Microsoft.AspNetCore.Http.Connections.Common\"",
    "\"Microsoft.AspNetCore.Hosting.Abstractions\"",
    "\"Microsoft.AspNetCore.Http.Abstractions\"",
    "\"Microsoft.AspNetCore.Hosting.Server.Abstractions\"",
    "\"Microsoft.AspNetCore.Http.Features\"",
    "\"Microsoft.Net.Http.Headers\"",
    "\"Microsoft.AspNetCore.SignalR.Core\"",
    "\"Microsoft.AspNetCore.SignalR.Protocols.Json\"",
    "\"Microsoft.AspNetCore.SignalR.Common\"",
    "\"Microsoft.AspNetCore.Connections.Abstractions\"",
    "\"Microsoft.Extensions.Features\"",
    "\"Microsoft.AspNetCore.DataProtection.Extensions\"",
    "\"Microsoft.AspNetCore.DataProtection\"",
    "\"Microsoft.AspNetCore.DataProtection.Abstractions\"",
    "\"Microsoft.AspNetCore.Cryptography.Internal\"",
    "\"Microsoft.AspNetCore.Components.Web\"",
    "\"Microsoft.JSInterop\"",
    "\"Microsoft.AspNetCore.Components.Forms\"",
    "\"Microsoft.AspNetCore.Components\"",
  }  # Add your filenames here
root_path = "./"  # Replace with your root directory

file_names = [ref + ".csproj" for ref in valid_references]

for file_name in file_names:
    file_path = find_file_in_tree(root_path, file_name)
    if file_path:
        if os.path.exists(file_path):
            if file_name.startswith("Microsoft"):
                new_name = file_name.replace("Microsoft\"", "Jokersoft\"", 1)  # Only replace the first occurrence
                file_path = rename_file(file_path, new_name)
            process_csproj(file_path, valid_references)
