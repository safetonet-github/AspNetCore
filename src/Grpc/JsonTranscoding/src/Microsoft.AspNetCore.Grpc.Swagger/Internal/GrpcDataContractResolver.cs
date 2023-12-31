// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Reflection;
using Google.Protobuf;
using Google.Protobuf.Reflection;
using Google.Protobuf.WellKnownTypes;
using Grpc.Shared;
using Swashbuckle.AspNetCore.SwaggerGen;
using Type = System.Type;

namespace Microsoft.AspNetCore.Grpc.Swagger.Internal;

internal sealed class GrpcDataContractResolver : ISerializerDataContractResolver
{
    private readonly ISerializerDataContractResolver _innerContractResolver;
    private readonly Dictionary<Type, MessageDescriptor> _messageTypeMapping;
    private readonly Dictionary<Type, EnumDescriptor> _enumTypeMapping;

    public GrpcDataContractResolver(ISerializerDataContractResolver innerContractResolver)
    {
        _innerContractResolver = innerContractResolver;
        _messageTypeMapping = new Dictionary<Type, MessageDescriptor>();
        _enumTypeMapping = new Dictionary<Type, EnumDescriptor>();
    }

    public DataContract GetDataContractForType(Type type)
    {
        if (!_messageTypeMapping.TryGetValue(type, out var messageDescriptor))
        {
            if (typeof(IMessage).IsAssignableFrom(type))
            {
                var property = type.GetProperty("Descriptor", BindingFlags.Public | BindingFlags.Static);
                messageDescriptor = property?.GetValue(null) as MessageDescriptor;

                if (messageDescriptor == null)
                {
                    throw new InvalidOperationException($"Couldn't resolve message descriptor for {type}.");
                }

                _messageTypeMapping[type] = messageDescriptor;
            }
        }

        if (messageDescriptor != null)
        {
            return ConvertMessage(messageDescriptor);
        }

        if (type.IsEnum)
        {
            if (_enumTypeMapping.TryGetValue(type, out var enumDescriptor))
            {
                var values = enumDescriptor.Values.Select(v => v.Name).ToList();
                return DataContract.ForPrimitive(type, DataType.String, dataFormat: null, value =>
                {
                    var match = enumDescriptor.Values.SingleOrDefault(v => v.Number == (int)value);
                    var name = match?.Name ?? value.ToString();
                    return @"""" + name + @"""";
                });
            }
        }

        return _innerContractResolver.GetDataContractForType(type);
    }

    private bool TryCustomizeMessage(MessageDescriptor messageDescriptor, [NotNullWhen(true)] out DataContract? dataContract)
    {
        // The messages serialized here should be kept in sync with SericeDescriptionHelper.IsCustomType.
        if (ServiceDescriptorHelpers.IsWellKnownType(messageDescriptor))
        {
            if (ServiceDescriptorHelpers.IsWrapperType(messageDescriptor))
            {
                var field = messageDescriptor.Fields[Int32Value.ValueFieldNumber];

                dataContract = _innerContractResolver.GetDataContractForType(MessageDescriptorHelpers.ResolveFieldType(field));
                return true;
            }
            if (messageDescriptor.FullName == Timestamp.Descriptor.FullName ||
                messageDescriptor.FullName == Duration.Descriptor.FullName ||
                messageDescriptor.FullName == FieldMask.Descriptor.FullName)
            {
                dataContract = DataContract.ForPrimitive(messageDescriptor.ClrType, DataType.String, dataFormat: null);
                return true;
            }
            if (messageDescriptor.FullName == Struct.Descriptor.FullName)
            {
                dataContract = DataContract.ForObject(messageDescriptor.ClrType, Array.Empty<DataProperty>(), extensionDataType: typeof(Value));
                return true;
            }
            if (messageDescriptor.FullName == ListValue.Descriptor.FullName)
            {
                dataContract = DataContract.ForArray(messageDescriptor.ClrType, typeof(Value));
                return true;
            }
            if (messageDescriptor.FullName == Value.Descriptor.FullName)
            {
                dataContract = DataContract.ForPrimitive(messageDescriptor.ClrType, DataType.Unknown, dataFormat: null);
                return true;
            }
            if (messageDescriptor.FullName == Any.Descriptor.FullName)
            {
                var anyProperties = new List<DataProperty>
                {
                    new DataProperty("@type", typeof(string), isRequired: true)
                };
                dataContract = DataContract.ForObject(messageDescriptor.ClrType, anyProperties, extensionDataType: typeof(Value));
                return true;
            }
        }

        dataContract = null;
        return false;
    }

    private DataContract ConvertMessage(MessageDescriptor messageDescriptor)
    {
        if (TryCustomizeMessage(messageDescriptor, out var dataContract))
        {
            return dataContract;
        }

        var properties = new List<DataProperty>();

        foreach (var field in messageDescriptor.Fields.InFieldNumberOrder())
        {
            // Enum type will later be used to call this contract resolver.
            // Register the enum type so we know to resolve its names from the descriptor.
            if (field.FieldType == FieldType.Enum)
            {
                _enumTypeMapping.TryAdd(field.EnumType.ClrType, field.EnumType);
            }

            Type fieldType;
            if (field.IsMap)
            {
                var mapFields = field.MessageType.Fields.InFieldNumberOrder();
                var valueType = MessageDescriptorHelpers.ResolveFieldType(mapFields[1]);
                fieldType = typeof(IDictionary<,>).MakeGenericType(typeof(string), valueType);
            }
            else if (field.IsRepeated)
            {
                fieldType = typeof(IList<>).MakeGenericType(MessageDescriptorHelpers.ResolveFieldType(field));
            }
            else
            {
                fieldType = MessageDescriptorHelpers.ResolveFieldType(field);
            }

            var propertyName = ServiceDescriptorHelpers.FormatUnderscoreName(field.Name, pascalCase: true, preservePeriod: false);
            var propertyInfo = messageDescriptor.ClrType.GetProperty(propertyName);

            properties.Add(new DataProperty(field.JsonName, fieldType, memberInfo: propertyInfo));
        }

        var schema = DataContract.ForObject(messageDescriptor.ClrType, properties: properties);

        return schema;
    }
}
