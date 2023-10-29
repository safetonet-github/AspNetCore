// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Jokersoft.AspNetCore.Server.Kestrel.Core;

namespace Microsoft.AspNetCore.Server.Kestrel.Core.Internal.Infrastructure;

internal sealed class ThrowingWasUpgradedWriteOnlyStream : WriteOnlyStream
{
    public override bool CanSeek => false;

    public override long Length => throw new NotSupportedException();

    public override long Position
    {
        get => throw new NotSupportedException();
        set => throw new NotSupportedException();
    }

    public override void Write(byte[] buffer, int offset, int count)
        => throw new InvalidOperationException(CoreStrings.ResponseStreamWasUpgraded);

    public override Task WriteAsync(byte[] buffer, int offset, int count, CancellationToken cancellationToken)
        => throw new InvalidOperationException(CoreStrings.ResponseStreamWasUpgraded);

    public override void Flush()
        => throw new InvalidOperationException(CoreStrings.ResponseStreamWasUpgraded);

    public override long Seek(long offset, SeekOrigin origin)
        => throw new NotSupportedException();

    public override void SetLength(long value)
        => throw new NotSupportedException();
}
